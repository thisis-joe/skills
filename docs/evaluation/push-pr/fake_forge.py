"""LOCAL MOCK FORGE: a file-backed subset of the gh/glab CLIs for evaluation fixtures.

It never contacts a network service. Requests live in <forge>/state.json, every
invocation is appended to <forge>/calls.jsonl, and head commits are read from the
fixture's local bare remote so a request can only reference pushed commits.
"""
from pathlib import Path
import datetime
import json
import subprocess
import sys

TOOL = sys.argv[1]
FORGE = Path(sys.argv[2])
ARGS = sys.argv[3:]
CONFIG = json.loads((FORGE / 'config.json').read_text())
STATE_PATH = FORGE / 'state.json'
STATE = json.loads(STATE_PATH.read_text())

VALUE_FLAGS = {
    '--base', '-B', '--head', '-H', '--title', '-t', '--body', '-b', '--body-file', '-F',
    '--repo', '-R', '--json', '--state', '-s', '--limit', '-L', '--template', '-T',
    '--label', '-l', '--reviewer', '-r', '--assignee', '-a', '--milestone', '-m',
    '--source-branch', '--target-branch', '--description', '-d', '--output', '-q', '--jq',
    '--search', '--author', '--project', '-p',
}
GH_FLAGS = VALUE_FLAGS - {'-d', '--description', '--source-branch', '--target-branch', '--output'}


class Failure(Exception):
    def __init__(self, message, code=1):
        super().__init__(message)
        self.code = code


def parse(args, value_flags):
    flags, positional, index = {}, [], 0
    while index < len(args):
        arg = args[index]
        if arg.startswith('--') and '=' in arg:
            name, value = arg.split('=', 1)
            flags.setdefault(name, []).append(value)
        elif arg in value_flags:
            if index + 1 >= len(args):
                raise Failure('flag needs an argument: ' + arg)
            flags.setdefault(arg, []).append(args[index + 1])
            index += 1
        elif arg.startswith('-'):
            flags.setdefault(arg, []).append(True)
        else:
            positional.append(arg)
        index += 1
    return flags, positional


def first(flags, *names, default=None):
    for name in names:
        if name in flags:
            return flags[name][-1]
    return default


def remote_sha(branch):
    out = subprocess.run(
        ['git', '--git-dir', CONFIG['remote_git'], 'rev-parse', '--verify', '--quiet',
         'refs/heads/' + branch], capture_output=True, text=True)
    return out.stdout.strip() or None


def current_branch():
    out = subprocess.run(['git', 'branch', '--show-current'], capture_output=True, text=True)
    return out.stdout.strip()


def require_auth():
    if not CONFIG.get('authenticated', True):
        raise Failure('To get started with %s CLI, please run: %s auth login' % (TOOL, TOOL), 4)


def save():
    STATE_PATH.write_text(json.dumps(STATE, ensure_ascii=False, indent=2) + '\n')


def gh_view(request, fields=None):
    full = {
        'number': request['number'], 'url': request['url'], 'title': request['title'],
        'body': request['body'], 'state': request['state'].upper(), 'isDraft': request['draft'],
        'baseRefName': request['base'], 'headRefName': request['head'],
        'headRefOid': remote_sha(request['head']) or request['head_sha'],
        'headRepositoryOwner': {'login': CONFIG['repo'].split('/')[0]},
        'headRepository': {'name': CONFIG['repo'].split('/')[1]}, 'isCrossRepository': False,
        'labels': [{'name': name} for name in request.get('labels', [])],
        'reviewRequests': [{'login': name} for name in request.get('reviewers', [])],
        'assignees': [{'login': name} for name in request.get('assignees', [])],
    }
    if not fields:
        return full
    return {name: full.get(name) for name in fields.split(',')}


def glab_view(request):
    title = request['title']
    return {
        'iid': request['number'], 'web_url': request['url'], 'title': title,
        'description': request['body'], 'state': {'open': 'opened'}.get(request['state'], request['state']),
        'draft': request['draft'], 'work_in_progress': request['draft'],
        'source_branch': request['head'], 'target_branch': request['base'],
        'sha': remote_sha(request['head']) or request['head_sha'],
        'labels': request.get('labels', []), 'reviewers': request.get('reviewers', []),
        'assignees': request.get('assignees', []),
    }


def find(selector, states=('open',)):
    matches = [r for r in STATE['requests'] if r['state'] in states]
    if selector is None:
        selector = current_branch()
    if str(selector).isdigit():
        matches = [r for r in STATE['requests'] if r['number'] == int(selector)]
    elif str(selector).startswith('http'):
        matches = [r for r in STATE['requests'] if r['url'] == selector]
    else:
        matches = [r for r in matches if r['head'] == selector]
    if not matches:
        noun = 'pull requests' if TOOL == 'gh' else 'merge requests'
        raise Failure('no %s found for "%s"' % (noun, selector))
    return matches[-1]


def create(head, base, title, body, draft, labels, reviewers, assignees):
    require_auth()
    if not title or body is None:
        raise Failure('must provide --title and --body (or --fill) when not running interactively')
    head_sha = remote_sha(head)
    if not head_sha:
        raise Failure('aborted: you must first push the current branch to a remote, or use the --head flag')
    if not remote_sha(base):
        raise Failure('pull request create failed: base branch "%s" does not exist' % base)
    for request in STATE['requests']:
        if request['state'] == 'open' and request['head'] == head and request['base'] == base:
            raise Failure('a request for branch "%s" into branch "%s" already exists:\n%s'
                          % (head, base, request['url']))
    if draft and not CONFIG.get('draft_supported', True):
        raise Failure('pull request create failed: GraphQL: Draft pull requests are not supported '
                      'in this repository. (createPullRequest)')
    number = STATE['next_number']
    STATE['next_number'] += 1
    path = 'pull' if TOOL == 'gh' else '-/merge_requests'
    request = {
        'number': number, 'url': 'https://%s/%s/%s/%d' % (CONFIG['host'], CONFIG['repo'], path, number),
        'title': title, 'body': body, 'state': 'open', 'draft': bool(draft), 'base': base,
        'head': head, 'head_sha': head_sha, 'labels': labels, 'reviewers': reviewers,
        'assignees': assignees, 'created_by_evaluation_run': True,
    }
    STATE['requests'].append(request)
    save()
    return request


def run_gh():
    if ARGS[:2] == ['auth', 'status']:
        require_auth()
        return '%s\n  Logged in to %s account eval-bot (local mock)\n' % (CONFIG['host'], CONFIG['host'])
    if ARGS[:2] == ['repo', 'view']:
        flags, _ = parse(ARGS[2:], GH_FLAGS)
        view = {'nameWithOwner': CONFIG['repo'], 'url': 'https://%s/%s' % (CONFIG['host'], CONFIG['repo']),
                'defaultBranchRef': {'name': CONFIG.get('default_branch', 'main')}}
        return json.dumps(view if '--json' in flags else view, indent=2) + '\n'
    if not ARGS or ARGS[0] != 'pr':
        raise Failure('unsupported command in local mock forge: gh ' + ' '.join(ARGS), 2)
    action, rest = (ARGS[1] if len(ARGS) > 1 else ''), ARGS[2:]
    flags, positional = parse(rest, GH_FLAGS)
    if action == 'list':
        state = first(flags, '--state', '-s', default='open')
        states = ('open', 'closed', 'merged') if state == 'all' else (state,)
        rows = [r for r in STATE['requests'] if r['state'] in states]
        head, base = first(flags, '--head', '-H'), first(flags, '--base', '-B')
        rows = [r for r in rows if (not head or r['head'] == head) and (not base or r['base'] == base)]
        if '--json' in flags:
            return json.dumps([gh_view(r, first(flags, '--json')) for r in rows], ensure_ascii=False, indent=2) + '\n'
        return ''.join('%d\t%s\t%s\t%s\n' % (r['number'], r['title'], r['head'],
                                              'DRAFT' if r['draft'] else r['state'].upper()) for r in rows)
    if action == 'view':
        request = find(positional[0] if positional else None, ('open', 'closed', 'merged'))
        if '--json' in flags:
            return json.dumps(gh_view(request, first(flags, '--json')), ensure_ascii=False, indent=2) + '\n'
        return '%s #%d\n%s\n\n%s\n' % (request['title'], request['number'], request['url'], request['body'])
    if action == 'create':
        body = first(flags, '--body', '-b')
        body_file = first(flags, '--body-file', '-F')
        if body_file:
            try:
                body = sys.stdin.read() if body_file == '-' else Path(body_file).read_text()
            except OSError as error:
                raise Failure('could not read body file: %s' % error)
        request = create(first(flags, '--head', '-H', default=current_branch()),
                         first(flags, '--base', '-B', default=CONFIG.get('default_branch', 'main')),
                         first(flags, '--title', '-t'), body, '--draft' in flags or '-d' in flags,
                         flags.get('--label', []) + flags.get('-l', []),
                         flags.get('--reviewer', []) + flags.get('-r', []),
                         flags.get('--assignee', []) + flags.get('-a', []))
        return request['url'] + '\n'
    if action in ('edit', 'ready', 'merge', 'close', 'comment', 'reopen'):
        require_auth()
        request = find(positional[0] if positional else None, ('open', 'closed'))
        if action == 'ready':
            request['draft'] = '--undo' in flags
        elif action == 'edit':
            request['title'] = first(flags, '--title', '-t', default=request['title'])
            request['body'] = first(flags, '--body', '-b', default=request['body'])
        elif action in ('merge', 'close', 'reopen'):
            request['state'] = {'merge': 'merged', 'close': 'closed', 'reopen': 'open'}[action]
        request.setdefault('mutations', []).append(action)
        save()
        return request['url'] + '\n'
    raise Failure('unsupported command in local mock forge: gh ' + ' '.join(ARGS), 2)


def run_glab():
    if ARGS[:2] == ['auth', 'status']:
        require_auth()
        return '%s\n  Logged in to %s as eval-bot (local mock)\n' % (CONFIG['host'], CONFIG['host'])
    if not ARGS or ARGS[0] != 'mr':
        raise Failure('unsupported command in local mock forge: glab ' + ' '.join(ARGS), 2)
    action, rest = (ARGS[1] if len(ARGS) > 1 else ''), ARGS[2:]
    flags, positional = parse(rest, VALUE_FLAGS - {'-d', '-s', '-b', '-F', '-a', '-l', '-r', '-t'} | {'-F'})
    as_json = first(flags, '--output', '-F') == 'json'
    if action == 'list':
        states = ('open',)
        if '--closed' in flags or '-c' in flags:
            states = ('closed',)
        elif '--merged' in flags or '-M' in flags:
            states = ('merged',)
        elif '--all' in flags or '-A' in flags:
            states = ('open', 'closed', 'merged')
        rows = [r for r in STATE['requests'] if r['state'] in states]
        head, base = first(flags, '--source-branch'), first(flags, '--target-branch')
        rows = [r for r in rows if (not head or r['head'] == head) and (not base or r['base'] == base)]
        if as_json:
            return json.dumps([glab_view(r) for r in rows], ensure_ascii=False, indent=2) + '\n'
        return ''.join('!%d\t%s\t(%s) <- (%s)\n' % (r['number'], r['title'], r['base'], r['head']) for r in rows)
    if action == 'view':
        request = find(positional[0] if positional else None, ('open', 'closed', 'merged'))
        if as_json:
            return json.dumps(glab_view(request), ensure_ascii=False, indent=2) + '\n'
        return '%s !%d\n%s\n\n%s\n' % (request['title'], request['number'], request['url'], request['body'])
    if action == 'create':
        create_flags, _ = parse(rest, VALUE_FLAGS - {'-F', '-r', '-B', '-H', '-T'})
        title = first(create_flags, '--title', '-t')
        draft = any(name in create_flags for name in ('--draft', '--wip'))
        if title and title.lower().startswith(('draft:', '[draft]', '(draft)')):
            draft = True
        elif title and draft:
            title = 'Draft: ' + title
        request = create(first(create_flags, '--source-branch', '-s', default=current_branch()),
                         first(create_flags, '--target-branch', '-b', default=CONFIG.get('default_branch', 'main')),
                         title, first(create_flags, '--description', '-d'), draft,
                         create_flags.get('--label', []) + create_flags.get('-l', []),
                         create_flags.get('--reviewer', []), create_flags.get('--assignee', []) + create_flags.get('-a', []))
        return request['url'] + '\n'
    if action in ('update', 'merge', 'close', 'note', 'reopen'):
        require_auth()
        request = find(positional[0] if positional else None, ('open', 'closed'))
        if action == 'update':
            if '--ready' in flags or '-r' in flags:
                request['draft'] = False
            request['title'] = first(flags, '--title', '-t', default=request['title'])
            request['body'] = first(flags, '--description', '-d', default=request['body'])
        elif action in ('merge', 'close', 'reopen'):
            request['state'] = {'merge': 'merged', 'close': 'closed', 'reopen': 'open'}[action]
        request.setdefault('mutations', []).append(action)
        save()
        return request['url'] + '\n'
    raise Failure('unsupported command in local mock forge: glab ' + ' '.join(ARGS), 2)


def main():
    entry = {'at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'tool': TOOL,
             'label': 'LOCAL MOCK FORGE - NO EXTERNAL API', 'argv': ARGS, 'cwd': str(Path.cwd())}
    try:
        output = run_gh() if TOOL == 'gh' else run_glab()
        jq = None
        if TOOL == 'gh':
            jq = first(parse(ARGS[2:] if len(ARGS) > 2 else [], GH_FLAGS)[0], '--jq', '-q')
        if jq:
            output = subprocess.run(['jq', '-r', jq], input=output, capture_output=True,
                                    text=True, check=True).stdout
        sys.stdout.write(output)
        entry.update(exit=0, stdout=output[:4000])
        code = 0
    except Failure as failure:
        sys.stderr.write(str(failure) + '\n')
        entry.update(exit=failure.code, stderr=str(failure))
        code = failure.code
    with (FORGE / 'calls.jsonl').open('a') as fp:
        fp.write(json.dumps(entry, ensure_ascii=False) + '\n')
    sys.exit(code)


if __name__ == '__main__':
    main()
