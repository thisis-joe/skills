"""Collect post-run evidence from the live fixtures and assess each case.

Usage: python3 collect_evidence.py <output-directory> <fixture-run-directory>...

Reads only the disposable fixture run (Git refs, mock forge and mock Jira files)
and writes copies plus assertions next to this script. It never reruns a skill,
pushes, or contacts a network service.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
OUT = Path(sys.argv[1]).resolve()
RUNS = [Path(arg).resolve() for arg in sys.argv[2:]]
SKILL_FILES = ['skills/coco-push/SKILL.md', 'skills/coco-push/references/branch-and-ticket.md',
               'skills/coco-push/references/pull-request.md', 'skills/coco-push/references/sync-and-push.md',
               'skills/_coco-shared/contracts.md', 'skills/coco-build/SKILL.md']
MUTATIONS = {'edit', 'ready', 'merge', 'close', 'comment', 'reopen', 'update', 'note'}
DEFAULT_SECTIONS = [('Summary', '요약', '개요'), ('Related issue', '관련 이슈'), ('Changes', '변경'),
                    ('Verification', '검증', '테스트'), ('Reviewer notes', '리뷰어')]


def git(*args, cwd=None):
    return subprocess.run(['git', *args], cwd=cwd, capture_output=True, text=True)


def remote_refs(case):
    out = git('--git-dir', str(case / 'remote.git'), 'for-each-ref', '--format=%(objectname) %(refname)').stdout
    return {line.split(' ', 1)[1]: line.split(' ', 1)[0] for line in out.strip().splitlines()}


def headings(body):
    return [line[3:].strip() for line in (body or '').splitlines() if line.startswith('## ')]


def assess(name, case, request):
    work = case / 'work'
    branch = git('branch', '--show-current', cwd=work).stdout.strip()
    head = git('rev-parse', 'HEAD', cwd=work).stdout.strip()
    status = git('status', '--porcelain=v1', '-uall', cwd=work).stdout
    before = {line.split(' ', 1)[1]: line.split(' ', 1)[0]
              for line in (case / 'before-refs.txt').read_text().strip().splitlines()}
    after = remote_refs(case)
    calls = [json.loads(line) for line in (case / 'forge/calls.jsonl').read_text().splitlines() if line]
    state = json.loads((case / 'forge/state.json').read_text())
    created = [r for r in state['requests'] if r.get('created_by_evaluation_run')]
    preexisting = [r for r in state['requests'] if not r.get('created_by_evaluation_run')]
    creates = [c for c in calls if len(c['argv']) > 1 and c['argv'][1] == 'create']
    mutations = [c for c in calls if len(c['argv']) > 1 and c['argv'][1] in MUTATIONS]
    original_branch = request['branch']
    pushed_refs = {ref: sha for ref, sha in after.items() if before.get(ref) != sha}
    a = {
        'no_request_mutation_commands': not mutations,
        'every_create_call_requested_draft': all('--draft' in c['argv'] or '-d' in c['argv'] and c['tool'] == 'gh'
                                                 for c in creates),
        'no_fill_flag': all('--fill' not in c['argv'] and '-f' not in c['argv'] for c in creates),
        'no_reviewers_assignees_labels': all(not (r['reviewers'] or r['assignees'] or r['labels']) for r in created),
        'preexisting_requests_untouched': all(not r.get('mutations') for r in preexisting),
        'develop_and_main_unchanged': all(after.get(ref) == before.get(ref)
                                          for ref in ('refs/heads/main', 'refs/heads/develop')),
    }
    if name == 'check_fails':
        # A preserved, recoverable merge state is the expected stop, not a dirty failure.
        a.update(not_pushed=not pushed_refs, no_create_call=not creates, no_request=not created)
    else:
        a['clean_worktree'] = not status
        final_ref = 'refs/heads/' + branch
        a.update(published_head=after.get(final_ref) == head,
                 develop_peer_integrated=git('merge-base', '--is-ancestor', request['develop_peer_commit'], head,
                                             cwd=work).returncode == 0)
    if name in ('gh_template', 'gh_default', 'glab_default_template'):
        request_ok = len(created) == 1
        pr = created[0] if request_ok else {}
        a.update(one_request_created=request_ok, created_as_draft=pr.get('draft') is True,
                 target_is_develop=pr.get('base') == 'develop', source_is_final_branch=pr.get('head') == branch,
                 head_is_pushed_commit=pr.get('head_sha') == head,
                 title_has_full_jira_key=request['jira_key'] in pr.get('title', ''))
        found = headings(pr.get('body'))
        if name == 'gh_template':
            expected = ['개요', '관련 이슈', '변경 내용', '테스트', '체크리스트']
            a.update(template_headings_in_order=found == expected,
                     reviewer_item_unticked='- [ ] 리뷰어 지정' in pr.get('body', ''))
        elif name == 'glab_default_template':
            expected = ['What does this MR do and why?', 'Related issues', 'How to set up and validate locally',
                        'MR acceptance checklist']
            a.update(default_md_headings_in_order=found == expected,
                     hotfix_template_not_used='Rollback plan' not in pr.get('body', ''))
        else:
            index = [next((i for i, h in enumerate(found) if any(k.lower() in h.lower() for k in keys)), None)
                     for keys in DEFAULT_SECTIONS]
            a.update(default_required_sections_in_order=None not in index and index == sorted(index),
                     no_screenshot_section_without_ui=not any('screenshot' in h.lower() or '스크린샷' in h
                                                              for h in found),
                     sync_record_present=request['develop_peer_commit'][:7] in pr.get('body', ''))
    if name == 'gh_existing_open':
        a.update(no_request_created=not created, existing_request_still_draft=preexisting[0]['draft'] is True,
                 existing_body_unchanged=preexisting[0]['body'] == '## 개요\n할인 초안\n')
    if name == 'gh_draft_unsupported':
        a.update(no_request_created=not created, draft_attempt_rejected=any(c['exit'] != 0 for c in creates))
    if name in ('renamed_with_old_pr', 'scope_drift_old_pr'):
        a.update(no_duplicate_request=not created, old_request_untouched=not preexisting[0].get('mutations'))
        if branch != original_branch:
            a['old_remote_branch_preserved'] = (after.get('refs/heads/' + original_branch)
                                                == before.get('refs/heads/' + original_branch))
            a['old_branch_request_looked_up'] = any(
                original_branch in c['argv'] and c['argv'][1] in ('list', 'view') for c in calls)
    if name == 'scope_drift_old_pr':
        a['renamed_for_scope_drift'] = branch != original_branch
    return {
        'behavior_assessment': 'passed' if all(a.values()) else 'failed', 'assertions': a,
        'local_branch': branch, 'renamed': branch != original_branch, 'head': head,
        'changed_remote_refs': pushed_refs, 'forge_calls': [c['argv'] for c in calls],
        'created_requests': created, 'jira_updates': sum(
            json.loads(line)['operation'] == 'update'
            for line in (case / 'jira/adapter.jsonl').read_text().splitlines() if line),
    }


def main():
    results, runs = {}, []
    for run in RUNS:
        results.update(collect_run(run))
        before = {}
        for line in (run / 'skill-hashes-before.txt').read_text().splitlines():
            sha, path = line.split('  ', 1)
            before[path.strip()] = sha
        runs.append({'commit': (run / 'skill-commit.txt').read_text().strip(), 'skill_hashes': before,
                     'cases': sorted(p.name for p in run.iterdir() if (p / 'request.json').is_file())})
    after = {path: hashlib.sha256((REPO / path).read_bytes()).hexdigest() for path in SKILL_FILES}
    summary = {
        'type': 'fresh-context forward application of coco-push draft PR/MR behavior',
        'runs': runs, 'skill_files_match_evaluated_version': all(r['skill_hashes'] == after for r in runs),
        'forge': 'LOCAL MOCK gh/glab CLI (fake_forge.py); no external API',
        'jira': 'LOCAL MOCK file-backed adapter; no external API', 'real_git': True,
        'results': {name: {'behavior_assessment': r['behavior_assessment'], 'renamed': r['renamed'],
                           'failed_assertions': [k for k, v in r['assertions'].items() if not v]}
                    for name, r in sorted(results.items())},
    }
    (OUT / 'result.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def collect_run(run):
    results = {}
    for case in sorted(p for p in run.iterdir() if (p / 'request.json').is_file()):
        request = json.loads((case / 'request.json').read_text())
        out = OUT / case.name
        out.mkdir(exist_ok=True)
        for rel in ('request.json', 'agent-report.md', 'before-refs.txt', 'forge/config.json', 'forge/state.json',
                    'forge/calls.jsonl', 'jira/tasks.json', 'jira/adapter.jsonl'):
            target = out / rel.replace('/', '-')
            shutil.copyfile(case / rel, target)
        (out / 'after-refs.txt').write_text(''.join('%s %s\n' % (sha, ref)
                                                    for ref, sha in sorted(remote_refs(case).items())))
        work = case / 'work'
        (out / 'work-state.txt').write_text(
            git('status', '-sb', cwd=work).stdout + '\n'
            + git('log', '--graph', '--oneline', '--decorate', '--all', '-15', cwd=work).stdout)
        git('bundle', 'create', str(out / 'work.bundle'), '--all', cwd=work)
        git('--git-dir', str(case / 'remote.git'), 'bundle', 'create', str(out / 'remote.bundle'), '--all')
        result = assess(case.name, case, request)
        (out / 'result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        results[case.name] = result
    return results


if __name__ == '__main__':
    main()
