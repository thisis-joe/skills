#!/usr/bin/env python3
"""Bounded forward application of coco-push to self-authored local fixtures."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path('/tmp/coco-push-validation').resolve()
ROOT.mkdir(exist_ok=True)
HOOKS = ROOT / 'empty-hooks'
HOOKS.mkdir(exist_ok=True)
CONFIG = ROOT / 'isolated.gitconfig'
CONFIG.write_text('')
ENV = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=str(CONFIG),
           GIT_CONFIG_SYSTEM='/dev/null', GIT_TERMINAL_PROMPT='0',
           PYTHONDONTWRITEBYTECODE='1')
for key in list(ENV):
    if key.startswith('GIT_') and key not in {
        'GIT_CONFIG_NOSYSTEM', 'GIT_CONFIG_GLOBAL', 'GIT_CONFIG_SYSTEM',
        'GIT_TERMINAL_PROMPT'}:
        del ENV[key]
LOG = ROOT / 'commands.jsonl'
RESULTS = {'scope': 'One bounded application to self-authored local fixtures; not a benchmark or blanket safety certification.',
           'environment': {'root': str(ROOT), 'git_config_global': str(CONFIG),
                           'git_config_nosystem': True, 'hooks': str(HOOKS),
                           'home_modified': False, 'network_remotes_used': False},
           'sources': [], 'cases': []}
SEQ = 0

def now():
    return datetime.now(timezone.utc).isoformat()

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def event(data):
    with LOG.open('a') as fp:
        fp.write(json.dumps(data, ensure_ascii=False) + '\n')

def run(cwd, args, *, stage, expect=(0,)):
    global SEQ
    cwd = Path(cwd).resolve()
    assert cwd == ROOT or ROOT in cwd.parents, cwd
    args = [str(x) for x in args]
    if args[0] == 'git':
        args[1:1] = ['-c', 'core.hooksPath=' + str(HOOKS),
                     '-c', 'commit.gpgsign=false', '-c', 'tag.gpgsign=false',
                     '-c', 'user.name=COCO Push Fixture',
                     '-c', 'user.email=coco-push-fixture@example.invalid']
    SEQ += 1
    result = subprocess.run(args, cwd=cwd, env=ENV, text=True, capture_output=True)
    record = dict(id=SEQ, timestamp=now(), stage=stage, cwd=str(cwd),
                  argv=args, exit_code=result.returncode,
                  stdout=result.stdout, stderr=result.stderr)
    event(record)
    if result.returncode not in expect:
        raise RuntimeError(f'command {SEQ} unexpected exit {result.returncode}: {args}\n{result.stdout}\n{result.stderr}')
    return result

def git(cwd, *args, stage='fixture', expect=(0,)):
    return run(cwd, ['git', *args], stage=stage, expect=expect)

def write(repo, relative, text, stage='fixture'):
    p = Path(repo) / relative
    assert ROOT in p.resolve().parents
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    event(dict(timestamp=now(), action='write', stage=stage, path=str(p), sha256=sha(p)))

BASE_APP = 'def greet(name):\n    return f"Hello, {name}"\n'
FEATURE_APP = 'def greet(name):\n    return f"Hello, {name}!"\n'
DEVELOP_APP = 'def greet(name):\n    return f"Hello, {name.strip()}"\n'
RESOLVED_APP = 'def greet(name):\n    return f"Hello, {name.strip()}!"\n'
CORE_TEST = '''import unittest
from app import greet

class CoreTests(unittest.TestCase):
    def test_greeting(self):
        self.assertTrue(greet("Ada").startswith("Hello, Ada"))
'''
FEATURE_TEST = '''import unittest
from app import greet

class FeatureTests(unittest.TestCase):
    def test_exclamation(self):
        self.assertTrue(greet("Ada").endswith("!"))
'''
TRIM_TEST = '''import unittest
from app import greet

class DevelopTests(unittest.TestCase):
    def test_whitespace(self):
        self.assertNotIn(" Ada ", greet(" Ada "))
'''

def commit(repo, paths, message):
    git(repo, 'add', '--', *paths)
    git(repo, 'commit', '-m', message)
    return git(repo, 'rev-parse', 'HEAD').stdout.strip()

def tests(repo, stage, expect=(0,)):
    before = SEQ
    r = run(repo, ['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-v'], stage=stage, expect=expect)
    return {'command_id': before + 1, 'exit_code': r.returncode,
            'result': 'passed' if r.returncode == 0 else 'failed',
            'stdout': r.stdout, 'stderr': r.stderr}

def make_case(number, name, *, both=False, dirty=False, failing=False, remote_feature=False):
    case_dir = ROOT / f'case-{number}'
    case_dir.mkdir()
    remote = case_dir / 'remote.git'
    seed = case_dir / 'seed'
    work = case_dir / 'work'
    git(case_dir, 'init', '--bare', '--initial-branch=develop', remote)
    git(case_dir, 'init', '--initial-branch=develop', seed)
    write(seed, 'app.py', BASE_APP)
    write(seed, 'quota.py', 'def allowed(amount):\n    return amount > 0\n')
    write(seed, 'notes.txt', 'Existing user notes.\n')
    write(seed, 'AGENTS.md', '# Fixture rules\n\nRequired check: `python3 -m unittest discover -s tests -v`.\nUse feature branches and one commit per work unit.\n')
    write(seed, 'tests/test_core.py', CORE_TEST)
    base = commit(seed, ['app.py', 'quota.py', 'notes.txt', 'AGENTS.md', 'tests/test_core.py'], 'Initial greeting project')
    git(seed, 'remote', 'add', 'origin', remote)
    git(seed, 'push', 'origin', 'HEAD:refs/heads/develop')
    if both:
        git(seed, 'push', 'origin', 'HEAD:refs/heads/dev')
    git(case_dir, 'clone', remote, work)
    git(work, 'switch', '-c', 'feature/topic')
    git(work, 'branch', '--set-upstream-to=origin/develop', 'feature/topic')
    write(work, 'app.py', FEATURE_APP)
    write(work, 'tests/test_feature.py', FEATURE_TEST)
    feature = commit(work, ['app.py', 'tests/test_feature.py'], 'Add friendly exclamation')
    baseline_test = tests(work, 'fixture-baseline')
    if remote_feature:
        git(work, 'push', 'origin', 'HEAD:refs/heads/feature/topic')
        write(work, 'feature-notes.txt', 'Exclamation is intentional and must be retained.\n')
        commit(work, ['feature-notes.txt'], 'Document feature behavior')
    if not both and not dirty:
        write(seed, 'app.py', DEVELOP_APP)
        write(seed, 'tests/test_develop.py', TRIM_TEST)
        paths = ['app.py', 'tests/test_develop.py']
        if failing:
            write(seed, 'tests/test_required_quota.py', '''import unittest
from quota import allowed

class RequiredQuotaTests(unittest.TestCase):
    def test_zero_contract(self):
        self.assertTrue(allowed(0), "Required quota contract remains unresolved")
''')
            paths.append('tests/test_required_quota.py')
        develop = commit(seed, paths, 'Normalize names and extend required checks')
        git(seed, 'push', 'origin', 'HEAD:refs/heads/develop')
    else:
        develop = base
    if dirty:
        write(work, 'notes.txt', 'Existing user notes.\nPrivate unsaved idea: preserve exactly.\n')
    result = dict(number=number, name=name, directory=str(case_dir), remote=str(remote),
                  work=str(work), requested_action='$coco-push for the current feature branch',
                  fixture=dict(base=base, feature=feature, remote_develop=develop,
                               baseline_required_tests=baseline_test),
                  decisions=[], checks=[], pushes=[], integration_rounds=0)
    RESULTS['cases'].append(result)
    return result

def snapshot(case, label):
    w = Path(case['work'])
    data = dict(branch=git(w, 'branch', '--show-current', stage=label).stdout.strip(),
                head=git(w, 'rev-parse', 'HEAD', stage=label).stdout.strip(),
                status=git(w, 'status', '--porcelain=v1', '-uall', stage=label).stdout,
                upstream=git(w, 'rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{upstream}', stage=label).stdout.strip(),
                remotes=git(w, 'ls-remote', '--heads', case['remote'], stage=label).stdout,
                staged_diff=git(w, 'diff', '--cached', '--stat', stage=label).stdout,
                unstaged_diff=git(w, 'diff', '--stat', stage=label).stdout,
                unmerged=git(w, 'ls-files', '-u', stage=label).stdout,
                git_operations={name: (w / '.git' / name).exists() for name in ['MERGE_HEAD', 'rebase-merge', 'rebase-apply', 'CHERRY_PICK_HEAD', 'REVERT_HEAD']},
                file_hashes={str(p.relative_to(w)): sha(p) for p in sorted(w.rglob('*'))
                             if p.is_file() and '.git' not in p.relative_to(w).parts})
    case[label] = data
    (Path(case['directory']) / f'{label}.json').write_text(json.dumps(data, indent=2))
    return data

def inspect(case):
    w = Path(case['work'])
    git(w, 'rev-parse', '--show-toplevel', stage='inspect')
    for args in [('remote', '-v'), ('remote', 'get-url', '--all', 'origin'),
                 ('remote', 'get-url', '--push', '--all', 'origin'),
                 ('config', '--local', '--list'), ('branch', '-vv')]:
        git(w, *args, stage='inspect')
    for relative in ['AGENTS.md', 'app.py', 'tests/test_core.py', 'tests/test_feature.py']:
        run(w, ['cat', relative], stage='inspect')
    git(w, 'check-ref-format', 'refs/heads/feature/topic', stage='inspect')
    refs = git(w, 'ls-remote', '--heads', 'origin', 'refs/heads/dev', 'refs/heads/develop', stage='inspect').stdout
    case['candidate_base_refs'] = refs
    case['push_destination'] = git(w, 'remote', 'get-url', '--push', '--all', 'origin', stage='inspect').stdout.strip()
    case['push_ref'] = 'refs/heads/feature/topic'

def fetch_oid(case, destination, ref, label):
    w = Path(case['work'])
    git(w, 'fetch', destination, ref, stage=label)
    oid = git(w, 'rev-parse', 'FETCH_HEAD', stage=label).stdout.strip()
    assert git(w, 'cat-file', '-t', oid, stage=label).stdout.strip() == 'commit'
    return oid

def integrate(case, oid, label, resolve=False, fail=False):
    w = Path(case['work'])
    case['integration_rounds'] += 1
    assert case['integration_rounds'] <= 3
    merge = git(w, 'merge', '--no-commit', '--no-edit', oid, stage=label, expect=(0, 1))
    case.setdefault('merges', []).append({'oid': oid, 'exit_code': merge.returncode, 'stdout': merge.stdout, 'stderr': merge.stderr})
    unmerged = git(w, 'ls-files', '-u', stage=label).stdout
    git(w, 'status', '--short', stage=label)
    if unmerged:
        assert resolve
        for spec in [':1:app.py', ':2:app.py', ':3:app.py']:
            git(w, 'show', spec, stage=label)
        for p in ['tests/test_core.py', 'tests/test_feature.py', 'tests/test_develop.py']:
            run(w, ['cat', p], stage=label)
        write(w, 'app.py', RESOLVED_APP, stage=label)
        case['decisions'].append('Resolve app.py by stripping the name and preserving the feature exclamation. Both regression tests express compatible intent.')
        git(w, 'diff', '--', 'app.py', stage=label)
        git(w, 'add', '--', 'app.py', stage=label)
    assert not git(w, 'ls-files', '-u', stage=label).stdout
    git(w, 'diff', '--check', stage=label)
    git(w, 'diff', '--cached', stage=label)
    git(w, 'grep', '-n', '-E', r'^(<<<<<<< |=======|>>>>>>> )', '--', '.', stage=label, expect=(1,))
    check = tests(w, label + '-required-check', expect=(1,) if fail else (0,))
    case['checks'].append(check)
    if fail:
        case['outcome'] = 'blocked_required_check_failed'
        case['decisions'].append('Required quota test fails in unchanged quota.py. Preserve staged resolution and MERGE_HEAD; no integration commit or push. No unrelated implementation fix or test weakening.')
        return False
    if (w / '.git' / 'MERGE_HEAD').exists():
        git(w, 'commit', '-m', 'Integrate fetched changes into feature/topic', stage=label)
    tests_final = tests(w, label + '-final-head-check')
    case['checks'].append(tests_final)
    case['verified_head'] = git(w, 'rev-parse', 'HEAD', stage=label).stdout.strip()
    return True

def get_refs(case, label):
    w = Path(case['work'])
    base = git(w, 'ls-remote', '--heads', 'origin', 'refs/heads/develop', stage=label).stdout.split()[0]
    target_rows = git(w, 'ls-remote', '--heads', case['push_destination'], case['push_ref'], stage=label).stdout.split()
    return base, target_rows[0] if target_rows else None

def readiness(case, label):
    w = Path(case['work'])
    verified = case['verified_head']
    assert git(w, 'rev-parse', 'HEAD', stage=label).stdout.strip() == verified
    git(w, 'merge-base', '--is-ancestor', case['fetched_develop'], verified, stage=label)
    assert not git(w, 'status', '--porcelain=v1', '-uall', stage=label).stdout
    assert not git(w, 'ls-files', '-u', stage=label).stdout
    assert not any((w / '.git' / n).exists() for n in ['MERGE_HEAD', 'rebase-merge', 'rebase-apply', 'CHERRY_PICK_HEAD', 'REVERT_HEAD'])
    current_base, _ = get_refs(case, label)
    assert current_base == case['fetched_develop'], 'Fixture unexpectedly advanced develop'

def push(case, label, expect=(0,)):
    assert len(case['pushes']) < 3
    w = Path(case['work'])
    oid = case['verified_head']
    r = git(w, 'push', case['push_destination'], oid + ':' + case['push_ref'], stage=label, expect=expect)
    case['pushes'].append(dict(oid=oid, destination=case['push_destination'], ref=case['push_ref'],
                              exit_code=r.returncode, stdout=r.stdout, stderr=r.stderr))
    return r

def verify_remote(case):
    _, target = get_refs(case, 'post-push-confirmation')
    assert target == case['verified_head']
    case['confirmed_remote_oid'] = target
    assert git(Path(case['work']), 'rev-parse', 'HEAD', stage='post-push-confirmation').stdout.strip() == target
    case['outcome'] = 'pushed_and_remote_oid_confirmed'

def apply_normal(case, *, race=False, fail=False):
    w = Path(case['work'])
    snapshot(case, 'initial')
    inspect(case)
    case['selected_base'] = 'origin/refs/heads/develop'
    case['decisions'].append('Only remote develop exists. Push feature/topic to its own same-name remote ref although upstream is origin/develop.')
    base, target = get_refs(case, 'fetch-refs')
    case['fetched_develop'] = fetch_oid(case, 'origin', 'refs/heads/develop', 'fetch-develop')
    if target:
        fetched_target = fetch_oid(case, case['push_destination'], case['push_ref'], 'fetch-target')
        case['initial_fetched_target'] = fetched_target
        git(w, 'merge-base', '--is-ancestor', fetched_target, 'HEAD', stage='target-containment')
    if not integrate(case, case['fetched_develop'], 'initial-integration', resolve=True, fail=fail):
        snapshot(case, 'final')
        return
    readiness(case, 'first-pre-push')
    if race:
        peer = Path(case['directory']) / 'peer'
        git(Path(case['directory']), 'clone', case['remote'], peer, stage='race-injection')
        git(peer, 'switch', '--track', 'origin/feature/topic', stage='race-injection')
        write(peer, 'peer.py', 'def peer_enabled():\n    return True\n', stage='race-injection')
        write(peer, 'tests/test_peer.py', 'import unittest\nfrom peer import peer_enabled\n\nclass PeerTests(unittest.TestCase):\n    def test_peer(self):\n        self.assertTrue(peer_enabled())\n', stage='race-injection')
        git(peer, 'add', '--', 'peer.py', 'tests/test_peer.py', stage='race-injection')
        git(peer, 'commit', '-m', 'Add concurrent peer capability', stage='race-injection')
        case['peer_head'] = git(peer, 'rev-parse', 'HEAD', stage='race-injection').stdout.strip()
        tests(peer, 'race-peer-check')
        git(peer, 'push', 'origin', 'HEAD:refs/heads/feature/topic', stage='race-injection')
        rejection = push(case, 'first-push-actual-race', expect=(1,))
        assert '[rejected]' in rejection.stderr and ('fetch first' in rejection.stderr or 'non-fast-forward' in rejection.stderr)
        case['decisions'].append('Observed actual push rejection caused by concurrent remote feature commit; fetch both refs, integrate peer commit, rerun required checks, retry a normal single-refspec push.')
        case['fetched_develop'] = fetch_oid(case, 'origin', 'refs/heads/develop', 'retry-fetch-develop')
        new_target = fetch_oid(case, case['push_destination'], case['push_ref'], 'retry-fetch-target')
        assert new_target == case['peer_head']
        integrate(case, new_target, 'retry-integration')
        git(w, 'merge-base', '--is-ancestor', new_target, case['verified_head'], stage='retry-containment')
        readiness(case, 'retry-pre-push')
        push(case, 'retry-push')
    else:
        push(case, 'push')
    verify_remote(case)
    snapshot(case, 'final')

def main():
    for relative in ['skills/coco-push/SKILL.md', 'skills/coco-push/references/sync-and-push.md', 'skills/_coco-shared/contracts.md']:
        source = Path('/Users/Joseph/workspaces/skills') / relative
        destination = ROOT / 'sources' / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        RESULTS['sources'].append({'path': str(source), 'captured_copy': str(destination), 'sha256': sha(source)})
    c1 = make_case(1, 'Only develop; upstream points to base; resolvable text conflict')
    apply_normal(c1)
    c2 = make_case(2, 'Concurrent remote feature advance after integration and verification', remote_feature=True)
    apply_normal(c2, race=True)
    c3 = make_case(3, 'Both dev/develop and no authoritative choice', both=True)
    snapshot(c3, 'initial')
    inspect(c3)
    c3['outcome'] = 'blocked_base_choice_required'
    c3['required_input'] = 'Choose origin/dev or origin/develop as the integration base.'
    c3['decisions'].append('No user/repository/PR choice is available; do not infer develop from upstream. No real user question sent during this no-input fixture.')
    snapshot(c3, 'final')
    c4 = make_case(4, 'Unrelated dirty tracked user file without ownership', dirty=True)
    snapshot(c4, 'initial')
    inspect(c4)
    git(Path(c4['work']), 'diff', '--', 'notes.txt', stage='dirty-inspection')
    c4['outcome'] = 'blocked_dirty_ownership_decision_required'
    c4['required_input'] = 'A safe disposition or user-owned isolation of notes.txt is needed before integration/publication.'
    c4['decisions'].append('notes.txt is unrelated and unowned for this invocation. No add/commit/stash/reset/clean is performed during application.')
    snapshot(c4, 'final')
    c5 = make_case(5, 'Required test failure after conflict resolution/integration', failing=True)
    apply_normal(c5, fail=True)
    for case in RESULTS['cases']:
        initial, final = case['initial'], case['final']
        assert initial['branch'] == final['branch'] == 'feature/topic'
        assert initial['upstream'] == final['upstream'] == 'origin/develop'
        if case['number'] in (3, 4):
            for key in ['head', 'status', 'remotes', 'file_hashes', 'git_operations']:
                assert initial[key] == final[key], (case['number'], key)
        if case['number'] == 5:
            assert initial['head'] == final['head']
            assert initial['remotes'] == final['remotes']
            assert final['git_operations']['MERGE_HEAD']
            assert not final['unmerged']
            assert not case['pushes']
        if case['number'] in (1, 2):
            initial_develop = [line for line in initial['remotes'].splitlines() if line.endswith('refs/heads/develop')][0]
            assert initial_develop in final['remotes'].splitlines()
            assert final['status'] == ''
    RESULTS['command_count'] = SEQ
    RESULTS['completed_at'] = now()
    (ROOT / 'results.json').write_text(json.dumps(RESULTS, indent=2, ensure_ascii=False))
    lines = ['# coco-push bounded forward application', '', RESULTS['scope'], '',
             'All fixtures, bare remotes, clones, configuration, hooks, and evidence are under `/tmp/coco-push-validation`. No network remotes, global config writes, user workspace changes, real user questions, or delegated agents were used.', '',
             'Every subprocess command records its argv, cwd, exit code, stdout, stderr, stage, and UTC timestamp in `commands.jsonl`. Initial/final snapshots include branch, HEAD, status, upstream, remote refs, Git operation state, index conflict state, and relevant file SHA-256 hashes. Source copies and source hashes are retained.', '',
             '| Case | Outcome | Integration rounds | Application pushes |', '|---|---|---:|---:|']
    for case in RESULTS['cases']:
        lines.append(f"| {case['number']}: {case['name']} | {case['outcome']} | {case['integration_rounds']} | {len(case['pushes'])} |")
    for case in RESULTS['cases']:
        lines += ['', f"## Case {case['number']}", '', f"Initial HEAD: `{case['initial']['head']}`. Final HEAD: `{case['final']['head']}`.", '', *['- ' + d for d in case['decisions']]]
        if case.get('required_input'):
            lines += ['', 'No-input outcome: ' + case['required_input']]
        if case.get('confirmed_remote_oid'):
            lines += ['', f"Remote `feature/topic` confirmed at `{case['confirmed_remote_oid']}`; develop unchanged by application."]
        if case['number'] == 5:
            lines += ['', 'The fixture intentionally adds a failing required quota contract check on remote develop, outside the resolved greeting conflict. Required unittest run exits 1. The application preserves its recoverable merge and does not publish or repair unrelated quota behavior.']
    lines += ['', '## Observations and limits', '',
              '- No skill defect was observed within these five constructed cases. Both/develop ambiguity and dirty ownership remain explicit no-input blockers.',
              '- Case 2 records an actual Git rejection (exit 1, `[rejected] ... (fetch first)`) and a subsequent successful normal push after integration and revalidation.',
              '- Case 5 establishes that a required check failure prevents publication; it does not establish broad failure diagnosis or arbitrary conflict safety.',
              '- Configuration isolation is per-process, with a temporary empty global config and hooks directory. HOME and CODEX_HOME are untouched.',
              '- The executor is the same model reading the skill; fixtures and regression checks are self-authored. This is a bounded application, not an independent benchmark or a general safety certificate.', '',
              'See `results.json` for source hashes, exact snapshots and check/push evidence; `commands.jsonl` for all command outputs.']
    (ROOT / 'report.md').write_text('\n'.join(lines) + '\n')
    print(json.dumps({'report': str(ROOT/'report.md'), 'results': str(ROOT/'results.json'),
                      'commands': SEQ, 'outcomes': [(c['number'], c['outcome']) for c in RESULTS['cases']]}, indent=2))

if __name__ == '__main__':
    main()
