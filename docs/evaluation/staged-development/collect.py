"""Retain completed native trials and derive auditable, bounded observations.

This collector does not grade skill compliance or infer human effort. Original
events and even surplus driver turns are preserved in the evidence archive.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile

from run import needs_followup


def read(path):
    return json.loads(Path(path).read_text())


def collect(root, output):
    root = Path(root)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    control = read(root / 'control.json')
    observations = []
    for trial in control['trials']:
        evidence = Path(trial['evidence'])
        result = read(evidence / 'result.json')  # Refuse an incomplete run.
        end = len(result['turns'])
        for turn in result['turns']:
            outcome = read(evidence / ('outcome-%d.json' % turn['turn']))
            has_commit = len(outcome['commits']['stdout'].splitlines()) > 1
            if (outcome['functional_pass'] and has_commit
                    and not needs_followup(turn['messages'])):
                end = turn['turn']
                break
        surplus = result['turns'][end:]
        # Only classify redundant resumes if their recorded Git state agrees.
        states = [read(evidence / ('outcome-%d.json' % n))
                  for n in range(end, len(result['turns']) + 1)]
        unchanged = all(s['commits'] == states[0]['commits']
                        and s['status'] == states[0]['status'] for s in states)
        if surplus and not unchanged:
            raise ValueError('Surplus turn changed recorded state: ' + trial['id'])
        events = []
        for path in sorted(evidence.glob('turn-*.events.jsonl')):
            events.extend(json.loads(line) for line in path.read_text().splitlines()
                          if line.strip().startswith('{'))
        actions = [e['item'] for e in events if e.get('type') == 'item.completed'
                   and e.get('item', {}).get('type') == 'command_execution']
        commands = [a.get('command', '') for a in actions]
        suspicious = [c for c in commands if '/.codex/skills' in c
                      or '/.claude/skills' in c or '/snapshots/' in c]
        # A triage aid only: reviewers inspect commands, not this heuristic alone.
        observations.append({
            'id': trial['id'], 'case': trial['case'], 'arm': trial['arm'],
            'functional_probe': result['outcome']['functional_pass'],
            'required_runtime': result['outcome']['required_runtime'],
            'raw_turns': len(result['turns']), 'logical_turns': end,
            'surplus_driver_turns': len(surplus),
            'surplus_recorded_git_unchanged': unchanged if surplus else None,
            'raw_seconds': result['total_seconds'],
            'logical_seconds': round(sum(t['seconds'] for t in result['turns'][:end]), 3),
            'raw_usage': [t['usage'] for t in result['turns']],
            'completed_commands': len(actions), 'suspicious_source_reads': suspicious,
            'guide_unchanged': result['guide_hashes_after'] ==
                (control['snapshots'][trial['arm']] if trial['arm'] != 'bare' else {}),
            'final': result['turns'][end-1]['messages'][-1],
            'outcome': result['outcome'],
        })

    with tempfile.TemporaryDirectory(prefix='coco-history-') as temp:
        bundles = Path(temp)
        for trial in control['trials']:
            subprocess.run(['git', 'bundle', 'create', str(bundles / (trial['id']+'.bundle')),
                            '--all'], cwd=trial['project'], check=True, capture_output=True)
        archive = output / 'native-evidence.tar.gz'
        with tarfile.open(archive, 'w:gz') as stream:
            for name in ['control.json', 'summary.json', 'execution.log', 'snapshots', 'records']:
                stream.add(root / name, arcname=name)
            for trial in control['trials']:
                project = Path(trial['project'])
                for path in sorted(project.rglob('*')):
                    relative = path.relative_to(project)
                    if not path.is_file() or any(p in {'.git', '.guide', '__pycache__'}
                                                 for p in relative.parts):
                        continue
                    stream.add(path, arcname='projects/'+trial['id']+'/'+relative.as_posix())
                stream.add(bundles / (trial['id']+'.bundle'),
                           arcname='history/'+trial['id']+'.bundle')
    result = {'schema': 1, 'source_head': control['source_head'],
              'published_git_head': control['published_git_head'],
              'published_integrity': control['published_integrity'], 'cli': control['cli'],
              'archive_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
              'observations': observations,
              'limits': 'Six heterogeneous matched cases; synthetic owner; no human-effort or speed claim. Runtime-gap is not browser-verified.'}
    (output / 'results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'trials': len(observations), 'archive_bytes': archive.stat().st_size,
                      'archive_sha256': result['archive_sha256']}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    collect(args.root, args.output)
