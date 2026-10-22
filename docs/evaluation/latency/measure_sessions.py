#!/usr/bin/env python3
"""Measure COCO skill invocations from Claude Code session records.

Only timestamps, message ids, token usage, tool-call ids and skill markers are
read for one project in one time window. Prompt text, tool arguments, results
and paths are never printed; sessions appear as short hashes.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import statistics
import sys

COMMAND = re.compile(r'<command-name>/?(coco-[a-z]+)</command-name>')


def parse_time(value):
    if not isinstance(value, str):
        return None
    try:
        moment = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        return None
    return moment if moment.tzinfo else moment.replace(tzinfo=timezone.utc)


def claude_slug(path):
    """Same rule as coco-tellmeskill's recent_skills.py; also covers C:\\ paths."""
    return re.sub(r'[^A-Za-z0-9]', '-', str(path))


def project_dirs(config, project):
    slug = claude_slug(project)
    projects = config / 'projects'
    if not projects.is_dir():
        return []
    return [d for d in projects.iterdir()
            if d.is_dir() and (d.name == slug or d.name.startswith(slug + '--claude-worktrees-'))]


def rows(path, since, until):
    try:
        with path.open(encoding='utf-8', errors='replace') as handle:
            for line in handle:
                try:
                    record = json.loads(line)
                except ValueError:
                    continue
                when = parse_time(record.get('timestamp')) if isinstance(record, dict) else None
                if when and since <= when <= until and not record.get('isSidechain'):
                    yield when, record
    except OSError:
        return


def blocks(record):
    content = (record.get('message') or {}).get('content')
    if isinstance(content, str):
        return [{'type': 'text', 'text': content}]
    return [b for b in content if isinstance(b, dict)] if isinstance(content, list) else []


def marker(record):
    for block in blocks(record):
        if record.get('type') == 'assistant' and block.get('type') == 'tool_use' \
                and block.get('name') == 'Skill':
            skill = (block.get('input') or {}).get('skill')
            if isinstance(skill, str) and skill.startswith('coco-'):
                return skill
        if record.get('type') == 'user' and block.get('type') == 'text':
            found = COMMAND.search(block.get('text') or '')
            if found:
                return found.group(1)
    return None


def human_prompt(record):
    """A person's message: not a tool result and not an injected skill body."""
    if record.get('type') != 'user' or record.get('isMeta'):
        return False
    parts = blocks(record)
    return bool(parts) and all(b.get('type') == 'text' for b in parts)


def measure(events, idle_cap):
    """Split one session into units from each marker to the next prompt or marker."""
    units, current = [], None
    for when, record in events:
        skill = marker(record)
        if skill or (current and human_prompt(record)):
            if current:
                units.append(current)
            current = None
            if not skill:
                continue
            current = {'skill': skill, 'start': when, 'last': when, 'elapsed': 0.0, 'active_s': 0.0,
                       'tokens': {}, 'tool_open': {}, 'tool_s': 0.0, 'tool_calls': 0}
            continue
        if not current:
            continue
        current['elapsed'] += min((when - current['last']).total_seconds(), idle_cap)
        current['last'] = when
        message = record.get('message') or {}
        if record.get('type') == 'assistant':
            # Active time stops at the last model response, not at the user's idle time.
            current['active_s'] = current['elapsed']
            ident = message.get('id')
            usage = message.get('usage') or {}
            if ident:
                current['tokens'][ident] = max(current['tokens'].get(ident, 0),
                                               usage.get('output_tokens') or 0)
        for block in blocks(record):
            if block.get('type') == 'tool_use':
                current['tool_calls'] += 1
                current['tool_open'][block.get('id')] = when
            elif block.get('type') == 'tool_result' and block.get('tool_use_id') in current['tool_open']:
                started = current['tool_open'].pop(block['tool_use_id'])
                current['tool_s'] += (when - started).total_seconds()
    if current:
        units.append(current)
    return units


def summary(unit, session):
    return {'skill': unit['skill'], 'session': session, 'start': unit['start'].isoformat(),
            'active_s': round(unit['active_s'], 1), 'api_calls': len(unit['tokens']),
            'output_tokens': sum(unit['tokens'].values()), 'tool_calls': unit['tool_calls'],
            'tool_s': round(unit['tool_s'], 1)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    default_config = os.environ.get('CLAUDE_CONFIG_DIR') or str(Path.home() / '.claude')
    parser.add_argument('--config-dir', type=Path, default=Path(default_config))
    parser.add_argument('--project', type=Path, required=True, help='project folder the sessions ran in')
    parser.add_argument('--since', type=parse_time, required=True, help='ISO time, e.g. 2026-10-21T00:00:00Z')
    parser.add_argument('--until', type=parse_time, required=True)
    parser.add_argument('--idle-cap', type=float, default=120.0, help='longest gap counted as active, in seconds')
    parser.add_argument('--subagents', action='store_true', help='also read subagent transcripts')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    if not args.since or not args.until:
        parser.exit(2, 'error: --since and --until must be ISO times\n')
    results = []
    for directory in project_dirs(args.config_dir, args.project.resolve()):
        pattern = '**/*.jsonl' if args.subagents else '*.jsonl'
        for path in sorted(directory.glob(pattern)):
            session = hashlib.sha256(str(path.relative_to(directory)).encode('utf-8')).hexdigest()[:8]
            events = sorted(rows(path, args.since, args.until), key=lambda item: item[0])
            results.extend(summary(unit, session) for unit in measure(events, args.idle_cap))
    results.sort(key=lambda item: item['start'])
    if args.json:
        json.dump(results, sys.stdout, indent=1)
        print()
        return
    for item in results:
        print('{skill:18} {session} {start:.19} active={active_s:6.1f}s calls={api_calls:3} '
              'out_tokens={output_tokens:6} tools={tool_calls:3} tool_s={tool_s:5.1f}'.format(**item))
    for skill in sorted({item['skill'] for item in results}):
        times = [item['active_s'] for item in results if item['skill'] == skill]
        print('median {}: {:.1f}s over {} run(s)'.format(skill, statistics.median(times), len(times)))


if __name__ == '__main__':
    main()
