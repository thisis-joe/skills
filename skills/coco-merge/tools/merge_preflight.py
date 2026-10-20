"""Report what merging a pushed branch into the default branch would land.

Fetches objects only: branches, tracking refs, FETCH_HEAD, the index and the
working tree stay unchanged. Exit 0 clear, 1 blocked, 2 unable to run; never
read 2 as clear.
"""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys

INTEGRATION_CANDIDATES = ('dev', 'develop')
BLOCKERS = ('branch_not_on_remote', 'head_mismatch', 'unpushed_commits', 'unknown_remote_commits',
            'nothing_to_merge', 'conflicts', 'integration_commits_carried',
            'integration_base_ambiguous')
WARNINGS = ('behind_target', 'uncommitted_changes_excluded', 'operation_in_progress',
            'no_local_branch', 'conflict_check_unavailable')
OPERATIONS = (('MERGE_HEAD', 'merge'), ('rebase-merge', 'rebase'), ('rebase-apply', 'rebase'),
              ('CHERRY_PICK_HEAD', 'cherry-pick'), ('REVERT_HEAD', 'revert'))


class PreflightError(Exception):
    pass


class Repo:
    def __init__(self, path):
        self.path = str(Path(path).resolve())
        self.path = self.text('rev-parse', '--show-toplevel').strip()

    def run(self, *args, ok=(0,)):
        result = subprocess.run(['git', '-C', self.path, *args], capture_output=True)
        if result.returncode not in ok:
            raise PreflightError('git %s failed: %s' % (args[0], os.fsdecode(result.stderr).strip()))
        return result

    def text(self, *args, ok=(0,)):
        return os.fsdecode(self.run(*args, ok=ok).stdout)

    def config(self, key):
        return self.text('config', '--get', key, ok=(0, 1)).strip() or None

    def oid(self, ref):
        value = self.text('rev-parse', '--verify', '--quiet', '--end-of-options',
                          ref + '^{commit}', ok=(0, 1)).strip()
        return value or None

    def is_ancestor(self, older, newer):
        return self.run('merge-base', '--is-ancestor', older, newer, ok=(0, 1)).returncode == 0

    def oids(self, *revisions):
        return self.text('rev-list', '--reverse', *revisions, '--').split()

    def commits(self, *revisions):
        rows = []
        output = self.text('log', '--reverse', '--format=%H%x1f%P%x1f%s', *revisions, '--')
        for line in output.splitlines():
            oid, parents, subject = line.split('\x1f', 2)
            rows.append({'oid': oid, 'parents': parents.split(), 'subject': subject})
        return rows


def branch_name(value):
    if not value or value.startswith('-') or subprocess.run(
            ['git', 'check-ref-format', '--branch', value], capture_output=True).returncode:
        raise PreflightError('invalid branch name: %r' % value)
    return value


def remote_refs(repo, remote, names):
    """Read the remote's current tips; tracking refs may be stale."""
    output = repo.text('ls-remote', '--', remote, *['refs/heads/' + name for name in names])
    found = {}
    for line in output.splitlines():
        oid, ref = line.split('\t', 1)
        found[ref[len('refs/heads/'):]] = oid
    return found


def remote_default(repo, remote):
    output = repo.text('ls-remote', '--symref', '--', remote, 'HEAD')
    match = re.search(r'^ref: refs/heads/(\S+)\tHEAD$', output, re.M)
    if not match:
        raise PreflightError('remote HEAD does not name a default branch; pass --target')
    return match.group(1)


def fetch_objects(repo, remote, names, expected):
    # --refmap= and --no-write-fetch-head fetch objects without moving any ref.
    repo.run('fetch', '--quiet', '--no-tags', '--no-write-fetch-head', '--refmap=', '--',
             remote, *['refs/heads/' + name for name in names])
    for name in names:
        if repo.oid(expected[name]) != expected[name]:
            raise PreflightError('remote %s changed during preflight; run it again' % name)


def local_state(repo):
    operations = []
    for marker, name in OPERATIONS:
        path = Path(repo.text('rev-parse', '--git-path', marker).strip())
        if not path.is_absolute():
            path = Path(repo.path) / path
        if path.exists() and name not in operations:
            operations.append(name)
    entries = repo.run('status', '--porcelain=v1', '-z', '--untracked-files=all').stdout.split(b'\0')
    dirty, index = 0, 0
    while index < len(entries):
        if entries[index]:
            dirty += 1
            if b'R' in entries[index][:2] or b'C' in entries[index][:2]:
                index += 1  # A rename or copy entry is followed by its source path.
        index += 1
    return {'operations': operations, 'dirty_paths': dirty}


def conflicts(repo, target, head):
    result = repo.run('merge-tree', '--write-tree', '--name-only', '--no-messages', '-z',
                      target, head, ok=(0, 1, 128, 129))
    if result.returncode > 1:
        return {'status': 'unavailable', 'paths': []}
    fields = [os.fsdecode(item) for item in result.stdout.split(b'\0')[1:] if item]
    return {'status': 'conflict' if result.returncode else 'clean', 'paths': sorted(set(fields))}


def update_merges(repo, rows, pushed, target_tip):
    """Forge "update branch" merges: own tip first, target history second."""
    known = {pushed} if pushed else set()
    benign = []
    for row in rows:
        parents = row['parents']
        if (len(parents) == 2 and (parents[0] in known or (pushed and repo.is_ancestor(parents[0], pushed)))
                and repo.is_ancestor(parents[1], target_tip)):
            known.add(row['oid'])
            benign.append(row)
    return benign


def preflight(path, remote=None, branch=None, target=None, integration=None,
              expect_head=None, max_list=50):
    repo = Repo(path)
    if branch is None:
        branch = repo.text('symbolic-ref', '--quiet', '--short', 'HEAD', ok=(0, 1)).strip()
        if not branch:
            raise PreflightError('detached HEAD; pass --branch')
    branch = branch_name(branch)
    if remote is None:
        remote = (repo.config('branch.%s.pushRemote' % branch) or repo.config('remote.pushDefault')
                  or repo.config('branch.%s.remote' % branch) or 'origin')
    if remote.startswith('-'):
        raise PreflightError('invalid remote: %r' % remote)
    target = branch_name(target or remote_default(repo, remote))
    if target == branch:
        raise PreflightError('the work branch is the default branch; nothing to merge into it')
    wanted = [branch, target]
    if integration not in (None, 'none'):
        wanted.append(branch_name(integration))
    elif integration is None:
        wanted.extend(name for name in INTEGRATION_CANDIDATES if name not in wanted)
    tips = remote_refs(repo, remote, wanted)
    if target not in tips:
        raise PreflightError('target branch %s is not on %s' % (target, remote))
    if integration not in (None, 'none') and integration not in tips:
        raise PreflightError('integration base %s is not on %s' % (integration, remote))

    blockers, warnings = [], []
    local_head = repo.oid('refs/heads/' + branch)
    state = local_state(repo)
    if state['operations']:
        warnings.append('operation_in_progress')
    if state['dirty_paths']:
        warnings.append('uncommitted_changes_excluded')
    if local_head is None:
        warnings.append('no_local_branch')

    candidates = [name for name in INTEGRATION_CANDIDATES if name in tips and name != target]
    if integration is None:
        if len(candidates) > 1:
            blockers.append('integration_base_ambiguous')
        integration = candidates[0] if len(candidates) == 1 else None
    elif integration == 'none' or integration == target:
        integration = None

    report = {'schema': 1, 'repository': repo.path, 'remote': remote, 'branch': branch,
              'target': target, 'integration_base': integration, 'local_head': local_head,
              'head': tips.get(branch), 'expected_head': expect_head,
              'target_tip': tips[target], 'integration_tip': tips.get(integration),
              'local': state}
    if branch not in tips:
        blockers.append('branch_not_on_remote')
        return finish(report, blockers, warnings)

    fetch_objects(repo, remote, [name for name in (branch, target, integration) if name], tips)
    head, target_tip = tips[branch], tips[target]
    if expect_head and repo.oid(expect_head) != head:
        blockers.append('head_mismatch')

    unpushed = repo.commits(head + '..' + local_head) if local_head else []
    # Target commits a forge update brought in are already on the target; skip them.
    remote_only = repo.commits(local_head + '..' + head, '^' + target_tip) if local_head else []
    benign = update_merges(repo, remote_only, local_head, target_tip)
    unknown = [row for row in remote_only if row not in benign]
    if unpushed:
        blockers.append('unpushed_commits')
    if unknown:
        blockers.append('unknown_remote_commits')

    incoming = repo.commits(target_tip + '..' + head)
    behind = len(repo.oids(head + '..' + target_tip))
    if not incoming:
        blockers.append('nothing_to_merge')
    elif behind:
        warnings.append('behind_target')

    carried, own, base, already_integrated = [], incoming, None, False
    if integration and incoming:
        base = repo.text('merge-base', head, tips[integration], ok=(0, 1)).strip() or None
        if base:
            already_integrated = base == head
            carried = repo.commits(target_tip + '..' + base)
            own = repo.commits(head, '^' + target_tip, '^' + base)
        if carried:
            blockers.append('integration_commits_carried')

    own = [row for row in own if row not in benign]
    merge = conflicts(repo, target_tip, head) if incoming else {'status': 'clean', 'paths': []}
    if merge['status'] == 'conflict':
        blockers.append('conflicts')
    elif merge['status'] == 'unavailable':
        warnings.append('conflict_check_unavailable')

    def listed(rows):
        return [{'oid': row['oid'], 'subject': row['subject']} for row in rows[:max_list]]

    report.update({
        'merge_base_with_integration': base,
        'branch_already_in_integration_base': already_integrated,
        'counts': {'incoming': len(incoming), 'own': len(own), 'carried': len(carried),
                   'behind': behind, 'unpushed': len(unpushed),
                   'remote_only': len(remote_only), 'update_merges': len(benign)},
        'incoming': listed(incoming), 'own': listed(own), 'carried': listed(carried),
        'unpushed': listed(unpushed), 'unknown_remote_commits': listed(unknown),
        'update_merges': listed(benign), 'conflicts': merge})
    return finish(report, blockers, warnings)


def finish(report, blockers, warnings):
    assert set(blockers) <= set(BLOCKERS) and set(warnings) <= set(WARNINGS)
    report.update({'status': 'blocked' if blockers else 'clear',
                   'blockers': blockers, 'warnings': warnings})
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--repo', default='.')
    parser.add_argument('--remote', help='push remote; default: pushRemote, pushDefault, upstream remote, origin')
    parser.add_argument('--branch', help='pushed work branch; default: current branch')
    parser.add_argument('--target', help="branch to merge into; default: the remote's default branch")
    parser.add_argument('--integration-base',
                        help='branch the work was synchronized with; default: remote dev/develop; "none" disables')
    parser.add_argument('--expect-head', help='PR/MR head commit reported by the forge')
    parser.add_argument('--max-list', type=int, default=50, help='commits listed per group')
    args = parser.parse_args()
    try:
        report = preflight(args.repo, args.remote, args.branch, args.target, args.integration_base,
                           args.expect_head, max(args.max_list, 0))
    except (PreflightError, OSError, ValueError) as exc:
        parser.exit(2, str(exc) + '\n')
    print(json.dumps(report, indent=2, ensure_ascii=False))
    sys.exit(1 if report['blockers'] else 0)


if __name__ == '__main__':
    main()
