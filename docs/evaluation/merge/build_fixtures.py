#!/usr/bin/env python3
"""Build the four coco-merge evaluation fixtures under a fresh directory.

Each case has a bare remote reached through a GitHub-looking URL
(`url.<path>.insteadOf`), the agent's working clone, a fixture `gh` on
bin/, its state and the user's request. Usage: build_fixtures.py <root>
"""
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
URL = 'https://github.example.test/acme/app.git'


def git(*args, cwd=None):
    return subprocess.run(['git', *args], cwd=cwd, check=True, capture_output=True,
                          text=True).stdout.strip()


def identity(repo):
    git('config', 'user.email', 'dev@example.test', cwd=repo)
    git('config', 'user.name', 'Fixture Dev', cwd=repo)


def commit(repo, name, content, message):
    path = Path(repo) / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    git('add', name, cwd=repo)
    git('commit', '-qm', message, cwd=repo)
    return git('rev-parse', 'HEAD', cwd=repo)


def setup(case):
    case.mkdir(parents=True)
    remote = case / 'remote.git'
    git('init', '-q', '--bare', '-b', 'main', str(remote))
    seed = case / 'seed'
    git('clone', '-q', str(remote), str(seed))
    identity(seed)
    commit(seed, 'README.md', '# app\n', 'Initial commit')
    commit(seed, 'app.py', 'def main():\n    return "ok"\n', 'Add app entry point')
    git('push', '-q', 'origin', 'main', cwd=seed)
    return remote, seed


def finish(case, remote, branch, state, request, edit=None):
    work = case / 'work'
    git('clone', '-q', str(remote), str(work))
    identity(work)
    git('config', 'url.%s.insteadOf' % remote, URL, cwd=work)
    git('remote', 'set-url', 'origin', URL, cwd=work)
    git('switch', '-q', branch, cwd=work)
    if edit:
        edit(work)
    subprocess.run(['rm', '-rf', str(case / 'seed')], check=True)
    state = {'remote': str(remote), 'next_number': 20, 'approvalsMissing': False,
             'repo': {'default': 'main', 'mergeCommitAllowed': True, 'squashMergeAllowed': True,
                      'rebaseMergeAllowed': True, 'deleteBranchOnMerge': False,
                      'requireUpToDate': False}, **state}
    (case / 'state.json').write_text(json.dumps(state, indent=2, ensure_ascii=False))
    (case / 'calls.jsonl').write_text('')
    (case / 'request.txt').write_text(request + '\n')
    bin_dir = case / 'bin'
    bin_dir.mkdir()
    wrapper = bin_dir / 'gh'
    wrapper.write_text('#!/bin/sh\nFAKE_GH_STATE="%s" exec python3 "%s" "$@"\n' % (
        case / 'state.json', HERE / 'fake_gh.py'))
    wrapper.chmod(0o755)
    refs = git('ls-remote', str(remote))
    (case / 'initial-remote-refs.txt').write_text(refs + '\n')


def pr(number, head, base, title, draft=False, state='OPEN'):
    return {'number': number, 'title': title, 'body': '', 'state': state, 'isDraft': draft,
            'url': 'https://github.example.test/acme/app/pull/%d' % number,
            'headRefName': head, 'baseRefName': base, 'mergeCommit': None, 'mergedAt': None,
            'mergedBy': None, 'autoMergeRequest': None}


PASSING = [{'name': 'test', 'required': True, 'conclusion': 'success'},
           {'name': 'lint', 'required': False, 'conclusion': 'success'}]


def draft_clean(case):
    remote, seed = setup(case)
    git('switch', '-qc', 'feat/old', cwd=seed)
    commit(seed, 'old.py', 'OLD = 1\n', 'Add old feature')
    git('switch', '-q', 'main', cwd=seed)
    git('merge', '-q', '--no-ff', '-m', 'Merge pull request #5 from acme/feat/old', 'feat/old', cwd=seed)
    git('push', '-q', 'origin', 'main', cwd=seed)
    git('switch', '-qc', 'feat/login-check', cwd=seed)
    commit(seed, 'login.py', 'def valid(name):\n    return bool(name)\n', 'Add login input validation')
    commit(seed, 'test_login.py', 'from login import valid\nassert valid("a")\n', 'Test login input validation')
    git('push', '-q', 'origin', 'feat/login-check', cwd=seed)
    merged = pr(5, 'feat/old', 'main', 'Add old feature', state='MERGED')
    finish(case, remote, 'feat/login-check',
           {'checks': PASSING, 'prs': [merged, pr(7, 'feat/login-check', 'main', '[APP-123] 로그인 입력 검증', draft=True)]},
           '/coco-merge 방금 푸시한 PR 디폴트 브랜치로 머지해줘')


def develop_carry(case):
    remote, seed = setup(case)
    git('switch', '-qc', 'develop', cwd=seed)
    commit(seed, 'payment.py', 'FLOW = "v2"\n', 'Rewrite payment flow (unreleased)')
    git('push', '-q', 'origin', 'develop', cwd=seed)
    git('switch', '-qc', 'feat/profile', cwd=seed)
    commit(seed, 'profile.py', 'def page():\n    return "profile"\n', 'Add profile page')
    git('push', '-q', 'origin', 'feat/profile', cwd=seed)
    finish(case, remote, 'feat/profile',
           {'checks': PASSING, 'prs': [pr(8, 'feat/profile', 'develop', '[APP-140] 프로필 페이지', draft=True)]},
           '/coco-merge 푸시한 PR을 디폴트 브랜치로 머지해줘')


def failing_check(case):
    remote, seed = setup(case)
    git('switch', '-qc', 'feat/cache', cwd=seed)
    commit(seed, 'cache.py', 'CACHE = {}\n', 'Cache user lookups')
    git('push', '-q', 'origin', 'feat/cache', cwd=seed)

    def local_edits(work):
        (work / 'app.py').write_text('def main():\n    return "ok"  # local experiment\n')
        (work / 'scratch.txt').write_text('notes\n')

    checks = [{'name': 'test', 'required': True, 'conclusion': 'failure'},
              {'name': 'lint', 'required': False, 'conclusion': 'success'}]
    finish(case, remote, 'feat/cache',
           {'checks': checks, 'prs': [pr(9, 'feat/cache', 'main', '[APP-151] 사용자 조회 캐시')]},
           '/coco-merge 이 브랜치 PR 머지해줘', edit=local_edits)


def no_pr_behind(case):
    remote, seed = setup(case)
    git('switch', '-qc', 'feat/search', cwd=seed)
    commit(seed, 'search.py', 'def search(q):\n    return [q]\n', 'Add search endpoint')
    git('push', '-q', 'origin', 'feat/search', cwd=seed)
    git('switch', '-q', 'main', cwd=seed)
    commit(seed, 'README.md', '# app\n\nFixed header.\n', 'Fix README header')
    git('push', '-q', 'origin', 'main', cwd=seed)
    state = {'checks': PASSING, 'prs': []}
    finish(case, remote, 'feat/search', state, '/coco-merge 푸시한 브랜치를 디폴트 브랜치에 머지해줘')
    data = json.loads((case / 'state.json').read_text())
    data['repo']['requireUpToDate'] = True
    (case / 'state.json').write_text(json.dumps(data, indent=2, ensure_ascii=False))


CASES = {'draft-clean': draft_clean, 'develop-carry': develop_carry,
         'failing-check': failing_check, 'no-pr-behind': no_pr_behind}


if __name__ == '__main__':
    root = Path(sys.argv[1]).resolve()
    for name, build in CASES.items():
        build(root / name)
    print(json.dumps({name: str(root / name) for name in CASES}, indent=2))
