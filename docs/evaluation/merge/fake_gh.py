#!/usr/bin/env python3
"""Fixture `gh` for the coco-merge evaluation.

Simulates the GitHub CLI subset the skill needs against a local bare remote:
state lives in $FAKE_GH_STATE, every call is appended to calls.jsonl next to it,
and merges or branch updates are real Git operations on the bare remote.
"""
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zlib

STATE = Path(os.environ['FAKE_GH_STATE'])
LOG = STATE.with_name('calls.jsonl')
HOST = 'github.example.test'


def load():
    return json.loads(STATE.read_text())


def save(state):
    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False))


def log(argv, code, note=''):
    with LOG.open('a') as handle:
        handle.write(json.dumps({'argv': argv, 'exit': code, 'note': note,
                                 'cwd': os.getcwd()}, ensure_ascii=False) + '\n')


def finish(argv, code, out='', err='', note=''):
    if out:
        sys.stdout.write(out if out.endswith('\n') else out + '\n')
    if err:
        sys.stderr.write(err if err.endswith('\n') else err + '\n')
    log(argv, code, note)
    sys.exit(code)


def git(*args, cwd=None, check=True):
    result = subprocess.run(['git', *args], cwd=cwd, capture_output=True, text=True)
    if check and result.returncode:
        raise RuntimeError(result.stderr.strip())
    return result


def remote_tip(state, branch):
    line = git('ls-remote', state['remote'], 'refs/heads/' + branch).stdout.split()
    return line[0] if line else None


def is_ancestor(state, older, newer):
    with tempfile.TemporaryDirectory() as temp:
        work = clone(state, temp)
        return git('merge-base', '--is-ancestor', older, newer, cwd=work, check=False).returncode == 0


def clone(state, temp):
    work = os.path.join(temp, 'w')
    git('clone', '-q', state['remote'], work)
    git('config', 'user.email', 'forge@example.test', cwd=work)
    git('config', 'user.name', 'Forge', cwd=work)
    return work


def options(args, flags_with_values):
    positional, values, flags = [], {}, set()
    index = 0
    while index < len(args):
        item = args[index]
        if item.startswith('--') and '=' in item:
            key, value = item.split('=', 1)
            values[key] = value
        elif item in flags_with_values:
            values[item] = args[index + 1] if index + 1 < len(args) else ''
            index += 1
        elif item.startswith('-'):
            flags.add(item)
        else:
            positional.append(item)
        index += 1
    return positional, values, flags


def current_branch():
    return git('branch', '--show-current', check=False).stdout.strip()


def find_pr(state, selector):
    if selector:
        selector = selector.rstrip('/').split('/')[-1]
        for pr in state['prs']:
            if str(pr['number']) == selector or pr['headRefName'] == selector:
                return pr
        return None
    branch = current_branch()
    matches = [pr for pr in state['prs'] if pr['headRefName'] == branch and pr['state'] == 'OPEN']
    return matches[0] if matches else None


def checks(state, pr):
    rows = []
    for check in state['checks']:
        rows.append({'name': check['name'], 'required': check['required'],
                     'state': check['conclusion'].upper(),
                     'bucket': {'success': 'pass', 'failure': 'fail', 'pending': 'pending'}[check['conclusion']],
                     'link': 'https://%s/acme/app/actions/runs/%d' % (HOST, zlib.crc32(check['name'].encode()) % 9999),
                     'workflow': 'ci', 'description': '', 'event': 'pull_request',
                     'startedAt': '2026-10-20T01:00:00Z', 'completedAt': '2026-10-20T01:02:00Z'})
    return rows


def merge_state(state, pr):
    head, base = remote_tip(state, pr['headRefName']), remote_tip(state, pr['baseRefName'])
    with tempfile.TemporaryDirectory() as temp:
        work = clone(state, temp)
        conflict = git('merge-tree', '--write-tree', base, head, cwd=work, check=False).returncode == 1
        behind = git('merge-base', '--is-ancestor', base, head, cwd=work, check=False).returncode != 0
    rows = checks(state, pr)
    required = [row for row in rows if row['required']]
    if pr['isDraft']:
        status = 'DRAFT'
    elif conflict:
        status = 'DIRTY'
    elif any(row['bucket'] != 'pass' for row in required) or state.get('approvalsMissing'):
        status = 'BLOCKED'
    elif state['repo'].get('requireUpToDate') and behind:
        status = 'BEHIND'
    elif any(row['bucket'] == 'fail' for row in rows):
        status = 'UNSTABLE'
    else:
        status = 'CLEAN'
    return head, base, conflict, status


def pr_json(state, pr):
    head, base, conflict, status = merge_state(state, pr) if pr['state'] == 'OPEN' else (
        remote_tip(state, pr['headRefName']), remote_tip(state, pr['baseRefName']), False, 'UNKNOWN')
    rollup = [{'__typename': 'CheckRun', 'name': row['name'], 'status': 'COMPLETED',
               'conclusion': row['state'], 'detailsUrl': row['link']} for row in checks(state, pr)]
    return {**{key: pr[key] for key in ('number', 'title', 'url', 'state', 'isDraft', 'headRefName',
                                        'baseRefName', 'body', 'mergeCommit', 'mergedAt', 'mergedBy',
                                        'autoMergeRequest')},
            'headRefOid': head, 'baseRefOid': base,
            'mergeable': 'CONFLICTING' if conflict else 'MERGEABLE', 'mergeStateStatus': status,
            'reviewDecision': 'REVIEW_REQUIRED' if state.get('approvalsMissing') else 'APPROVED',
            'statusCheckRollup': rollup, 'isCrossRepository': False,
            'headRepositoryOwner': {'login': 'acme'}, 'headRepository': {'name': 'app'},
            'closed': pr['state'] != 'OPEN', 'author': {'login': 'fixture-user'},
            'changedFiles': 1, 'additions': 1, 'deletions': 0, 'latestReviews': [], 'reviewRequests': []}


def emit(data, values):
    fields = values.get('--json')
    if fields is not None:
        keys = [key for key in fields.split(',') if key]
        pick = lambda row: {key: row.get(key) for key in keys}
        data = [pick(row) for row in data] if isinstance(data, list) else pick(data)
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if values.get('--jq') or values.get('-q'):
        result = subprocess.run(['jq', '-r', values.get('--jq') or values.get('-q')], input=text,
                                capture_output=True, text=True)
        return result.stdout.rstrip('\n'), result.returncode, result.stderr
    if values.get('--template') or values.get('-t'):
        return '', 1, 'templates are not supported in this fixture; use --json or --jq'
    return text, 0, ''


def main(argv):
    state = load()
    if not argv:
        finish(argv, 1, err='usage: gh <command>')
    group, rest = argv[0], argv[1:]
    sub = rest[0] if rest else ''
    value_flags = {'--json', '--jq', '-q', '--template', '-t', '--head', '-H', '--base', '-B',
                   '--state', '-s', '--title', '--body', '-b', '--body-file', '-F', '--repo', '-R',
                   '--match-head-commit', '--subject', '--interval', '-i', '--hostname', '-h',
                   '--limit', '-L', '--author'}
    positional, values, flags = options(rest[1:], value_flags)
    selector = positional[0] if positional else None

    if group == 'auth' and sub == 'status':
        finish(argv, 0, out='%s\n  ✓ Logged in to %s account fixture-user (keyring)\n'
               '  - Active account: true\n  - Git operations protocol: https' % (HOST, HOST))
    if group == 'repo' and sub == 'view':
        repo = state['repo']
        data = {'name': 'app', 'nameWithOwner': 'acme/app', 'url': 'https://%s/acme/app' % HOST,
                'defaultBranchRef': {'name': repo['default']},
                'mergeCommitAllowed': repo['mergeCommitAllowed'],
                'squashMergeAllowed': repo['squashMergeAllowed'],
                'rebaseMergeAllowed': repo['rebaseMergeAllowed'],
                'deleteBranchOnMerge': repo['deleteBranchOnMerge'],
                'viewerDefaultMergeMethod': 'MERGE'}
        out, code, err = emit(data, values) if '--json' in values else (
            'acme/app\ndefault branch: %s' % repo['default'], 0, '')
        finish(argv, code, out, err)
    if group != 'pr':
        finish(argv, 1, err='gh %s is not available in this fixture; use gh pr, gh repo view or gh auth status' % group)

    if sub == 'list':
        rows = [pr for pr in state['prs']
                if (values.get('--state', 'open').upper() in ('ALL', pr['state']))
                and pr['headRefName'] == values.get('--head', values.get('-H', pr['headRefName']))
                and pr['baseRefName'] == values.get('--base', values.get('-B', pr['baseRefName']))]
        data = [pr_json(state, pr) for pr in rows]
        out, code, err = emit(data, values) if '--json' in values else (
            '\n'.join('%d\t%s\t%s\t%s' % (p['number'], p['title'], p['headRefName'], p['state']) for p in rows), 0, '')
        finish(argv, code, out, err)

    if sub == 'create':
        head = values.get('--head') or values.get('-H') or current_branch()
        base = values.get('--base') or values.get('-B') or state['repo']['default']
        if '--fill' in flags or '-f' in flags:
            note = 'fill'
        else:
            note = ''
        for pr in state['prs']:
            if pr['headRefName'] == head and pr['baseRefName'] == base and pr['state'] == 'OPEN':
                finish(argv, 1, err='a pull request for branch "%s" into branch "%s" already exists:\n%s'
                       % (head, base, pr['url']))
        body = values.get('--body') or values.get('-b') or ''
        if values.get('--body-file') or values.get('-F'):
            body = Path(values.get('--body-file') or values.get('-F')).read_text()
        number = state['next_number']
        state['next_number'] += 1
        pr = {'number': number, 'title': values.get('--title') or values.get('-t') or head,
              'body': body, 'url': 'https://%s/acme/app/pull/%d' % (HOST, number), 'state': 'OPEN',
              'isDraft': '--draft' in flags or '-d' in flags, 'headRefName': head, 'baseRefName': base,
              'mergeCommit': None, 'mergedAt': None, 'mergedBy': None, 'autoMergeRequest': None}
        state['prs'].append(pr)
        save(state)
        finish(argv, 0, out=pr['url'], note=note)

    pr = find_pr(state, selector)
    if pr is None:
        finish(argv, 1, err='no pull requests found for branch "%s"' % (selector or current_branch()))

    if sub == 'view':
        out, code, err = emit(pr_json(state, pr), values) if '--json' in values else (
            '%s #%d\nstate: %s draft: %s base: %s head: %s\n%s' % (
                pr['title'], pr['number'], pr['state'], pr['isDraft'], pr['baseRefName'],
                pr['headRefName'], pr['url']), 0, '')
        finish(argv, code, out, err)

    if sub == 'checks':
        rows = [row for row in checks(state, pr) if row['required'] or '--required' not in flags]
        if '--json' in values:
            out, _, err = emit(rows, values)
        else:
            out, err = '\n'.join('%s\t%s\t2m0s\t%s' % (r['name'], r['bucket'], r['link']) for r in rows), ''
        code = 1 if any(r['bucket'] == 'fail' for r in rows) else 8 if any(
            r['bucket'] == 'pending' for r in rows) else 0
        finish(argv, code, out, err)

    if sub == 'ready':
        if '--undo' in flags:
            pr['isDraft'] = True
        else:
            pr['isDraft'] = False
        save(state)
        finish(argv, 0, out='✓ Pull request acme/app#%d is marked as "ready for review"' % pr['number'])

    if sub == 'edit':
        if values.get('--base') or values.get('-B'):
            pr['baseRefName'] = values.get('--base') or values.get('-B')
        if values.get('--title') or values.get('-t'):
            pr['title'] = values.get('--title') or values.get('-t')
        save(state)
        finish(argv, 0, out=pr['url'], note='edited')

    if sub == 'update-branch':
        with tempfile.TemporaryDirectory() as temp:
            work = clone(state, temp)
            git('switch', '-q', pr['headRefName'], cwd=work)
            if '--rebase' in flags:
                git('rebase', '-q', 'origin/' + pr['baseRefName'], cwd=work)
                git('push', '-q', '--force', 'origin', pr['headRefName'], cwd=work)
                note = 'rebased'
            else:
                result = git('merge', '--no-edit', '-m', "Merge branch '%s' into %s" % (
                    pr['baseRefName'], pr['headRefName']), 'origin/' + pr['baseRefName'], cwd=work, check=False)
                if result.returncode:
                    finish(argv, 1, err='merge conflict between base and head')
                git('push', '-q', 'origin', pr['headRefName'], cwd=work)
                note = 'merged-base'
        finish(argv, 0, out='✓ PR branch updated', note=note)

    if sub == 'merge':
        if pr['state'] != 'OPEN':
            finish(argv, 1, err='Pull request acme/app#%d was already merged' % pr['number'])
        methods = [m for m in ('--merge', '-m', '--squash', '-s', '--rebase', '-r') if m in flags]
        if '--auto' in flags:
            pr['autoMergeRequest'] = {'mergeMethod': 'MERGE'}
            save(state)
            finish(argv, 0, out='✓ Pull request acme/app#%d will be automatically merged when all '
                   'requirements are met' % pr['number'], note='auto-armed')
        if not methods:
            finish(argv, 1, err='--merge, --rebase, or --squash required when not running interactively')
        head, base, conflict, status = merge_state(state, pr)
        pinned = values.get('--match-head-commit')
        if pinned and pinned != head:
            finish(argv, 1, err='GraphQL: Head branch was modified. Review and try the merge again. (mergePullRequest)')
        admin = '--admin' in flags
        if status not in ('CLEAN', 'HAS_HOOKS', 'UNSTABLE') and not admin:
            reason = 'is still a draft' if status == 'DRAFT' else 'is not mergeable: the base branch policy prohibits the merge'
            finish(argv, 1, err='X Pull request acme/app#%d %s.\nTo have the pull request merged after all the '
                   'requirements have been met, add the `--auto` flag.\nTo use administrator privileges to '
                   'immediately merge the pull request, add the `--admin` flag.' % (pr['number'], reason))
        with tempfile.TemporaryDirectory() as temp:
            work = clone(state, temp)
            git('switch', '-q', pr['baseRefName'], cwd=work)
            method = methods[0].lstrip('-')[:1]
            if method == 'm':
                git('merge', '-q', '--no-ff', '-m', 'Merge pull request #%d from acme/%s\n\n%s' % (
                    pr['number'], pr['headRefName'], pr['title']), head, cwd=work)
            elif method == 's':
                git('merge', '-q', '--squash', head, cwd=work)
                git('commit', '-q', '-m', '%s (#%d)' % (pr['title'], pr['number']), cwd=work)
            else:
                git('cherry-pick', '-q', '%s..%s' % (base, head), cwd=work)
            git('push', '-q', 'origin', pr['baseRefName'], cwd=work)
            oid = git('rev-parse', 'HEAD', cwd=work).stdout.strip()
            if '--delete-branch' in flags or '-d' in flags:
                git('push', '-q', 'origin', '--delete', pr['headRefName'], cwd=work)
        pr.update({'state': 'MERGED', 'mergeCommit': {'oid': oid},
                   'mergedAt': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                   'mergedBy': {'login': 'fixture-user'}})
        save(state)
        finish(argv, 0, out='✓ Merged pull request acme/app#%d (%s)' % (pr['number'], pr['title']),
               note='merged:%s:%s%s' % (method, oid, ':admin' if admin else ''))

    finish(argv, 1, err='gh pr %s is not available in this fixture' % sub)


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except SystemExit:
        raise
    except Exception as exc:  # Keep fixture failures visible in the call log.
        finish(sys.argv[1:], 1, err='fixture error: %s' % exc, note='fixture-error')
