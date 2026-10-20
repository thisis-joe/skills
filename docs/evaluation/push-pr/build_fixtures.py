"""Build disposable local fixtures for the coco-push draft PR/MR evaluation.

Usage: python3 build_fixtures.py <empty-output-directory> [case ...]

The first run used the first seven cases; `scope_drift_old_pr` was added and run
separately after `renamed_with_old_pr` kept its adequate name.

Every remote is a local bare repository reached through a repository-local
`url.<path>.insteadOf` rewrite of a reserved `.test` forge URL. The forge CLI and
Jira are local file-backed mocks; nothing here contacts a network service.
"""
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ENV = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1',
           GIT_AUTHOR_NAME='fixture', GIT_AUTHOR_EMAIL='fixture@example.test',
           GIT_COMMITTER_NAME='fixture', GIT_COMMITTER_EMAIL='fixture@example.test')
CHECK = ['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-v']

PRICING = '''def subtotal(items):
    """Sum (unit_price, quantity) pairs."""
    return sum(price * quantity for price, quantity in items)
'''
PRICING_TEST = '''import unittest
from src.pricing import subtotal


class SubtotalTests(unittest.TestCase):
    def test_sums_lines(self):
        self.assertEqual(subtotal([(10, 2), (5, 1)]), 25)
'''
ROUNDING = '''from decimal import Decimal, ROUND_HALF_UP


def to_cents(amount):
    return int(Decimal(str(amount)).scaleb(2).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
'''
ROUNDING_TEST = '''import unittest
from src.rounding import to_cents


class RoundingTests(unittest.TestCase):
    def test_half_up(self):
        self.assertEqual(to_cents(1.005), 101)
'''
DISCOUNT = '''from src.pricing import subtotal


def apply_discount(items, percent):
    """Return the subtotal after a percentage discount."""
    if not 0 <= percent <= 100:
        raise ValueError('percent must be between 0 and 100')
    return subtotal(items) * (100 - percent) / 100
'''
DISCOUNT_TEST = '''import unittest
from src.discount import apply_discount


class DiscountTests(unittest.TestCase):
    def test_applies_percentage(self):
        self.assertEqual(apply_discount([(10, 2)], 10), 18)

    def test_rejects_out_of_range(self):
        with self.assertRaises(ValueError):
            apply_discount([(10, 1)], 120)
'''
DISCOUNT_DOC = '''# Discounts

`apply_discount(items, percent)` applies a 0-100 percentage discount to the subtotal.
'''
COUPON = '''CODES = {'WELCOME10': 10, 'VIP20': 20}


def coupon_percent(code):
    """Validate a coupon code and return its discount percentage."""
    normalized = code.strip().upper()
    if normalized not in CODES:
        raise KeyError('unknown coupon: ' + code)
    return CODES[normalized]
'''
COUPON_TEST = '''import unittest
from src.coupon import coupon_percent


class CouponTests(unittest.TestCase):
    def test_normalizes_code(self):
        self.assertEqual(coupon_percent(' welcome10 '), 10)

    def test_rejects_unknown(self):
        with self.assertRaises(KeyError):
            coupon_percent('NOPE')
'''
PRICING_SKIP = '''def subtotal(items):
    """Sum (unit_price, quantity) pairs, ignoring non-positive quantities."""
    return sum(price * quantity for price, quantity in items if quantity > 0)
'''
PRICING_SKIP_TEST = PRICING_TEST + '''
    def test_ignores_non_positive_quantities(self):
        self.assertEqual(subtotal([(10, 2), (10, -1)]), 20)
'''
RETURNS_TEST = '''import unittest
from src.pricing import subtotal


class ReturnsTests(unittest.TestCase):
    def test_negative_quantity_is_a_return(self):
        """Settled returns policy: a negative quantity refunds that line."""
        self.assertEqual(subtotal([(10, 2), (10, -1)]), 10)
'''
GH_TEMPLATE = '''## 개요
<!-- 무엇을, 왜 바꿨는지 2~3문장으로 적어주세요. -->

## 관련 이슈
<!-- Jira 키와 링크 -->

## 변경 내용
-

## 테스트
- [ ] 단위 테스트 통과
- [ ] 수동 확인

## 체크리스트
- [ ] 리뷰어 지정
- [ ] 문서 갱신 필요 여부 확인
'''
GL_DEFAULT = '''## What does this MR do and why?
<!-- Describe the change and the problem it solves. -->

## Related issues
<!-- Jira key -->

## How to set up and validate locally
<!-- Commands and results. -->

## MR acceptance checklist
- [ ] Tests added or updated
- [ ] Documentation updated if needed
'''
GL_HOTFIX = '''## Hotfix
Incident link:
Rollback plan:
'''


def run(args, cwd, capture=False):
    result = subprocess.run(args, cwd=cwd, env=ENV, check=True, text=True,
                            capture_output=True)
    return result.stdout.strip() if capture else None


def write(root, files):
    for name, text in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)


def commit(root, message, files=None, remove=()):
    if files:
        write(root, files)
    for name in remove:
        run(['git', 'rm', '-q', name], root)
    run(['git', 'add', '-A'], root)
    run(['git', 'commit', '-q', '-m', message], root)
    return run(['git', 'rev-parse', 'HEAD'], root, capture=True)


def agents_md(forge):
    host, tool = forge
    name = 'GitLab' if tool == 'glab' else 'GitHub Enterprise'
    return (
        '# Repository rules\n\n'
        '- Development base: `develop` on `origin`. Work branches use `type(part)/number-Summary`.\n'
        '- Required check: `python3 -m unittest discover -s tests -v`.\n'
        f'- Forge: {name} at `{host}` (repository `acme/widget`); use the `{tool}` CLI.\n'
        '- Jira project `WID`; read and update tasks only through the local adapter named in request.json.\n'
    )


def build_case(out, name, spec):
    case = out / name
    seed, bare, work = case / 'seed', case / 'remote.git', case / 'work'
    for folder in ('bin', 'forge', 'jira'):
        (case / folder).mkdir(parents=True)
    host, tool = spec['forge']
    url = f'https://{host}/acme/widget.git'

    seed.mkdir()
    run(['git', 'init', '-q', '-b', 'main'], seed)
    base_files = {'AGENTS.md': agents_md(spec['forge']), '.gitignore': '__pycache__/\n',
                  'src/__init__.py': '', 'tests/__init__.py': '', 'src/pricing.py': PRICING,
                  'tests/test_pricing.py': PRICING_TEST}
    base_files.update(spec.get('template_files', {}))
    commit(seed, 'chore: initial widget pricing', base_files)
    run(['git', 'branch', 'develop'], seed)

    branch = spec['branch']
    run(['git', 'checkout', '-q', '-b', branch, 'develop'], seed)
    published = None
    for index, (message, files) in enumerate(spec['feature_commits']):
        sha = commit(seed, message, files)
        if index + 1 == spec.get('published_commits', 0):
            published = sha
    run(['git', 'checkout', '-q', 'develop'], seed)
    develop_peer = commit(seed, spec.get('develop_message', 'feat: add half-up cent rounding'),
                          spec.get('develop_files', {'src/rounding.py': ROUNDING,
                                                     'tests/test_rounding.py': ROUNDING_TEST}))

    run(['git', 'init', '-q', '--bare', '-b', 'main', str(bare)], case)
    run(['git', 'push', '-q', str(bare), 'main', 'develop'], seed)
    if published:
        run(['git', 'push', '-q', str(bare), f'{published}:refs/heads/{branch}'], seed)

    run(['git', 'clone', '-q', '--no-checkout', str(bare), str(work)], case)
    run(['git', 'remote', 'set-url', 'origin', url], work)
    run(['git', 'config', f'url.{bare}.insteadOf', url], work)
    run(['git', 'config', 'user.name', 'fixture-dev'], work)
    run(['git', 'config', 'user.email', 'fixture-dev@example.test'], work)
    run(['git', 'fetch', '-q', str(seed), f'refs/heads/{branch}:refs/heads/{branch}'], work)
    run(['git', 'checkout', '-q', branch], work)
    if published:
        run(['git', 'branch', '-q', '--set-upstream-to', f'origin/{branch}'], work)
    shutil.rmtree(seed)

    forge_config = {'label': 'LOCAL MOCK FORGE - NO EXTERNAL API', 'host': host,
                    'repo': 'acme/widget', 'remote_git': str(bare), 'default_branch': 'main',
                    'draft_supported': spec.get('draft_supported', True), 'authenticated': True}
    (case / 'forge/config.json').write_text(json.dumps(forge_config, indent=2) + '\n')
    requests = []
    for request in spec.get('open_requests', []):
        head_sha = run(['git', '--git-dir', str(bare), 'rev-parse', 'refs/heads/' + request['head']],
                       case, capture=True)
        path = 'pull' if tool == 'gh' else '-/merge_requests'
        requests.append(dict(request, url=f'https://{host}/acme/widget/{path}/{request["number"]}',
                             state='open', head_sha=head_sha, labels=[], reviewers=[], assignees=[]))
    state = {'requests': requests, 'next_number': 40}
    (case / 'forge/state.json').write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n')
    (case / 'forge/calls.jsonl').write_text('')
    wrapper = case / 'bin' / tool
    wrapper.write_text(f'#!/bin/sh\nexec python3 "{HERE / "fake_forge.py"}" {tool} "{case / "forge"}" "$@"\n')
    wrapper.chmod(0o755)

    shutil.copy(HERE / 'jira_adapter.py', case / 'jira/adapter.py')
    (case / 'jira/config.json').write_text(json.dumps(
        {'label': 'LOCAL MOCK JIRA - NO EXTERNAL API', 'reject_updates': False}) + '\n')
    (case / 'jira/tasks.json').write_text(json.dumps(
        {spec['jira']['key']: dict(spec['jira'], version=1)}, ensure_ascii=False, indent=2) + '\n')
    (case / 'jira/adapter.jsonl').write_text('')

    request = {
        'request': spec.get('request', '$coco-push로 이 브랜치를 origin/develop 기준으로 최신화하고 검증한 뒤 푸시해줘.'),
        'fixture_constraints': (
            f'Work only inside {case}. Prefix every shell command with '
            f'`export PATH="{case / "bin"}:$PATH"` so `{tool}` is the local mock forge. '
            f'Jira is the local mock: `python3 {case / "jira/adapter.py"} {case} read|search-number|update <arg> [patch.json]`. '
            'Never contact a real network service. Record any genuinely missing decision and stop there.'),
        'jira_key': spec['jira']['key'], 'branch': branch, 'check': CHECK,
        'develop_peer_commit': develop_peer,
    }
    (case / 'request.json').write_text(json.dumps(request, ensure_ascii=False, indent=2) + '\n')
    refs = run(['git', '--git-dir', str(bare), 'for-each-ref', '--format=%(objectname) %(refname)'],
               case, capture=True)
    (case / 'before-refs.txt').write_text(refs + '\n')
    return case


GH = ('github.example.test', 'gh')
GL = ('gitlab.example.test', 'glab')
DISCOUNT_COMMITS = [
    ('feat: add percentage discount', {'src/discount.py': DISCOUNT, 'tests/test_discount.py': DISCOUNT_TEST}),
    ('docs: describe discounts', {'docs/discount.md': DISCOUNT_DOC}),
]
DISCOUNT_TASK = {
    'key': 'WID-123', 'summary': '할인_적용',
    'description': '요구사항\n- 소계에 0~100% 비율 할인을 적용한다.\n- 범위를 벗어난 비율은 거절한다.\n'
                   '수용 조건\n- 10% 할인 시 20 -> 18\n- 120%는 ValueError',
}
CASES = {
    'gh_template': dict(forge=GH, branch='feat(be)/123-할인_적용', feature_commits=DISCOUNT_COMMITS,
                        jira=DISCOUNT_TASK, template_files={'.github/pull_request_template.md': GH_TEMPLATE}),
    'gh_default': dict(forge=GH, branch='feat(be)/123-할인_적용', feature_commits=DISCOUNT_COMMITS,
                       jira=DISCOUNT_TASK),
    'gh_existing_open': dict(
        forge=GH, branch='feat(be)/123-할인_적용', feature_commits=DISCOUNT_COMMITS, published_commits=1,
        jira=DISCOUNT_TASK,
        open_requests=[{'number': 12, 'title': '[WID-123] 할인_적용', 'body': '## 개요\n할인 초안\n',
                        'draft': True, 'base': 'develop', 'head': 'feat(be)/123-할인_적용'}]),
    'glab_default_template': dict(
        forge=GL, branch='feat(be)/123-할인_적용', feature_commits=DISCOUNT_COMMITS, jira=DISCOUNT_TASK,
        template_files={'.gitlab/merge_request_templates/Default.md': GL_DEFAULT,
                        '.gitlab/merge_request_templates/Hotfix.md': GL_HOTFIX}),
    'gh_draft_unsupported': dict(forge=GH, branch='feat(be)/123-할인_적용', feature_commits=DISCOUNT_COMMITS,
                                 jira=DISCOUNT_TASK, draft_supported=False),
    'check_fails': dict(
        forge=GH, branch='feat(be)/123-할인_적용',
        feature_commits=[('feat: ignore non-positive quantities and add discount',
                          {'src/pricing.py': PRICING_SKIP, 'tests/test_pricing.py': PRICING_SKIP_TEST,
                           'src/discount.py': DISCOUNT, 'tests/test_discount.py': DISCOUNT_TEST})],
        develop_message='test: settle negative quantities as returns',
        develop_files={'tests/test_returns.py': RETURNS_TEST},
        jira=dict(DISCOUNT_TASK, description=DISCOUNT_TASK['description'] + '\n- 수량이 0 이하인 줄은 무시한다.')),
    'renamed_with_old_pr': dict(
        forge=GH, branch='feat(be)/131-할인_적용', published_commits=1,
        feature_commits=DISCOUNT_COMMITS[:1] + [
            ('feat: validate coupon codes for discounts', {'src/coupon.py': COUPON, 'tests/test_coupon.py': COUPON_TEST})],
        jira={'key': 'WID-131', 'summary': '할인_적용',
              'description': '요구사항\n- 소계에 0~100% 비율 할인을 적용한다.\n'
                             '- 쿠폰 코드를 검증해 할인율을 결정한다(공백 제거, 대소문자 무시).\n'
                             '- 후속: 쿠폰 만료일 관리는 이번 범위가 아니다.\n'
                             '수용 조건\n- 10% 할인 시 20 -> 18\n- welcome10 -> 10%\n- 알 수 없는 코드는 거절'},
        open_requests=[{'number': 21, 'title': '[WID-131] 할인_적용', 'body': '## 개요\n할인 초안\n',
                        'draft': True, 'base': 'develop', 'head': 'feat(be)/131-할인_적용'}]),
    'scope_drift_old_pr': dict(
        forge=GH, branch='feat(be)/141-쿠폰_만료일_표시', published_commits=1,
        feature_commits=[
            ('feat: validate coupon codes', {'src/coupon.py': COUPON}),
            ('test: cover coupon code validation', {'tests/test_coupon.py': COUPON_TEST})],
        jira={'key': 'WID-141', 'summary': '쿠폰_만료일_표시',
              'description': '원래 요구사항\n- 쿠폰 목록에 만료일을 표시한다.\n'
                             '범위 변경 (2026-10-15 기획 합의)\n'
                             '- 만료일 표시는 WID-150으로 이관하고 이번 작업에서 구현하지 않는다.\n'
                             '- 이번 작업은 쿠폰 코드 검증으로 대체한다: 공백 제거, 대소문자 무시, 알 수 없는 코드는 거절.\n'
                             '수용 조건\n- welcome10 -> 10%\n- 알 수 없는 코드는 거절'},
        open_requests=[{'number': 21, 'title': '[WID-141] 쿠폰_만료일_표시', 'body': '## 개요\n초안\n',
                        'draft': True, 'base': 'develop', 'head': 'feat(be)/141-쿠폰_만료일_표시'}]),
}


def main():
    out = Path(sys.argv[1]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    if any(out.iterdir()):
        sys.exit('output directory must be empty')
    for name in sys.argv[2:] or CASES:
        print(build_case(out, name, CASES[name]))


if __name__ == '__main__':
    main()
