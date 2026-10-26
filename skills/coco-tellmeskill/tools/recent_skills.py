#!/usr/bin/env python3
"""List skills recently invoked in this workspace from the runtime's own session records.

Workspace metadata scopes invocation records; only identifiers with their last-use
timestamps are printed. Prompt text and arguments are never printed.
"""
import argparse
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import re
import sys

# SKILL.md documents the window and count; change both together.
DEFAULT_DAYS = 30
DEFAULT_LIMIT = 3
COMMAND = re.compile(r'<command-name>/?([^<\s]+)</command-name>')
SELECTED = re.compile(r'^\s*<skill>\s*<name>([^<\s]+)</name>')


def names(values):
    """Accept repeated and comma-separated identifiers."""
    return {name.strip() for value in values or () for name in value.split(',') if name.strip()}


def parse_time(value):
    if not isinstance(value, str):
        return None
    try:
        moment = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        return None
    return moment if moment.tzinfo else moment.replace(tzinfo=timezone.utc)


def records(path, marker):
    """Yield parsed lines containing a marker; unreadable or malformed lines are skipped."""
    try:
        with path.open(encoding='utf-8', errors='replace') as handle:
            for line in handle:
                if marker(line):
                    try:
                        record = json.loads(line)
                    except ValueError:
                        continue
                    if isinstance(record, dict):
                        yield record
    except OSError:
        return


def recent_files(directory, cutoff, pattern):
    """Files modified inside the window; older files cannot hold newer events."""
    if not directory.is_dir():
        return []
    found = []
    for path in directory.glob(pattern):
        try:
            if path.is_file() and path.stat().st_mtime >= cutoff.timestamp():
                found.append(path)
        except OSError:
            continue
    return found


def texts(content):
    if isinstance(content, str):
        yield content
    elif isinstance(content, list):
        for item in content:
            if isinstance(item, dict) and isinstance(item.get('text'), str):
                yield item['text']


def claude_slug(path):
    """Claude Code names a project's record directory after its path."""
    return re.sub(r'[^A-Za-z0-9]', '-', str(path))


def claude_events(config, workspaces, cutoff):
    projects = config / 'projects'
    slugs = {claude_slug(path) for path in workspaces}
    if not projects.is_dir():
        return
    for directory in projects.iterdir():
        # The workspace itself and Claude Code worktrees created inside it.
        if not any(directory.name == slug or directory.name.startswith(slug + '--claude-worktrees-')
                   for slug in slugs):
            continue
        for path in recent_files(directory, cutoff, '*.jsonl'):
            for record in records(path, lambda line: '"Skill"' in line or 'command-name>' in line):
                # Project directory slugs collide, e.g. /app.one and /app-one.
                # Unknown record identity cannot establish workspace ownership.
                if not inside(record.get('cwd'), workspaces):
                    continue
                when = record.get('timestamp')
                message = record.get('message')
                if not isinstance(message, dict):
                    continue
                content = message.get('content')
                if record.get('type') == 'assistant' and isinstance(content, list):
                    for item in content:
                        if (isinstance(item, dict) and item.get('type') == 'tool_use'
                                and item.get('name') == 'Skill'
                                and isinstance(item.get('input'), dict)
                                and isinstance(item['input'].get('skill'), str)):
                            yield item['input']['skill'], when
                elif record.get('type') == 'user':
                    for text in texts(content):
                        for name in COMMAND.findall(text):
                            yield name, when


def inside(path, workspaces):
    # Non-strict resolution need not reject malformed filesystem strings.
    if not isinstance(path, str) or '\x00' in path:
        return False
    try:
        candidate = Path(path)
        if not candidate.is_absolute():
            return False
        candidate = candidate.resolve()
    except (TypeError, ValueError, OSError, RuntimeError):
        return False
    return any(candidate == root or root in candidate.parents for root in workspaces)


def codex_events(config, workspaces, cutoff):
    for path in recent_files(config / 'sessions', cutoff, '**/*.jsonl'):
        try:
            with path.open(encoding='utf-8', errors='replace') as handle:
                first = json.loads(handle.readline() or 'null')
        except (OSError, ValueError):
            continue
        # Sessions are attributed by the directory they started in; others stay unread.
        if not isinstance(first, dict) or first.get('type') != 'session_meta':
            continue
        meta = first.get('payload')
        if not isinstance(meta, dict) or not inside(meta.get('cwd'), workspaces):
            continue
        for record in records(path, lambda line: '<skill>' in line):
            payload = record.get('payload')
            if record.get('type') != 'response_item' or not isinstance(payload, dict) or \
                    payload.get('type') != 'message' or payload.get('role') != 'user':
                continue
            metadata = payload.get('internal_chat_message_metadata_passthrough')
            kinds = metadata.get('content_item_kinds') if isinstance(metadata, dict) else None
            if not isinstance(kinds, list):
                continue
            content = payload.get('content')
            items = content if isinstance(content, list) else [content]
            for item, kind in zip(items, kinds):
                if kind == 'skills.selected_skill_instructions':
                    for text in texts([item] if isinstance(item, dict) else item):
                        selected = SELECTED.match(text)
                        if selected:
                            yield selected.group(1), record.get('timestamp')


def recent_skills(runtime, config, workspace, days, limit, available, exclude):
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    workspaces = {Path(os.path.abspath(workspace)), Path(workspace).resolve()}
    events = claude_events if runtime == 'claude' else codex_events
    latest = {}
    for name, when in events(config, workspaces, cutoff):
        moment = parse_time(when)
        if moment is None or moment < cutoff or name in exclude:
            continue
        if available and name not in available:
            continue
        if name not in latest or moment > latest[name][0]:
            latest[name] = (moment, when)
    ordered = sorted(latest.items(), key=lambda item: (-item[1][0].timestamp(), item[0]))
    return [{'name': name, 'last_used': when} for name, (_, when) in ordered[:limit]]


def default_config(runtime):
    if runtime == 'claude':
        return Path(os.environ.get('CLAUDE_CONFIG_DIR') or Path.home() / '.claude')
    return Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex')


def main(argv=None):
    # Korean branch names and note sections must print on Windows consoles and pipes too.
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime', choices=('claude', 'codex'), required=True)
    parser.add_argument('--workspace', default=os.getcwd(),
                        help='workspace whose sessions are read (default: current directory)')
    parser.add_argument('--config-dir', type=Path,
                        help='runtime home (default: $CLAUDE_CONFIG_DIR or ~/.claude, '
                             '$CODEX_HOME or ~/.codex)')
    parser.add_argument('--days', type=int, default=DEFAULT_DAYS)
    parser.add_argument('--limit', type=int, default=DEFAULT_LIMIT)
    parser.add_argument('--available', action='append',
                        help='keep only these catalog identifiers (comma-separated, repeatable)')
    parser.add_argument('--exclude', action='append', help='identifiers to omit')
    args = parser.parse_args(argv)
    if args.days < 1 or args.limit < 1:
        parser.error('--days and --limit must be positive')
    config = args.config_dir or default_config(args.runtime)
    workspace = os.path.abspath(args.workspace)
    skills = recent_skills(args.runtime, config, workspace, args.days, args.limit,
                           names(args.available), names(args.exclude))
    json.dump({'runtime': args.runtime, 'workspace': workspace, 'days': args.days,
               'skills': skills}, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write('\n')


if __name__ == '__main__':
    main()
