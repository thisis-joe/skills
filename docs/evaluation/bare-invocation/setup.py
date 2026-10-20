"""Build isolated fixture repositories and agent prompts for bare-invocation cases."""
import argparse
import re
import subprocess
from pathlib import Path

BASE = Path(__file__).resolve().parent

README = """# Order pricing

Requirements:
- Members get 10% off.
- Orders of 3 or more items get 5% off for everyone, members or not.
- Discounts add up (at most 15%). Totals are integer won, rounded down.
"""

PRICING_BASE = """def total(unit_price, qty, member):
    rate = 0
    if member:
        rate += 10
    if qty >= 3:
        rate += 5
    return unit_price * qty * (100 - rate) // 100
"""

# Uncommitted refactor that drops the bulk discount for non-members.
PRICING_CHANGED = """BULK_QTY = 3


def discount_rate(qty, member):
    rate = 0
    if member:
        rate += 10
        if qty >= BULK_QTY:
            rate += 5
    return rate


def total(unit_price, qty, member):
    return unit_price * qty * (100 - discount_rate(qty, member)) // 100
"""

TESTS = """import unittest

from pricing import total


class PricingTests(unittest.TestCase):
    def test_member(self):
        self.assertEqual(total(100, 1, True), 90)

    def test_bulk_member(self):
        self.assertEqual(total(100, 3, True), 255)

    def test_bulk_nonmember(self):
        self.assertEqual(total(100, 3, False), 285)


if __name__ == '__main__':
    unittest.main()
"""


def run(cwd, *args):
    subprocess.run(args, cwd=cwd, check=True, capture_output=True)


def make_repo(path):
    path.mkdir(parents=True)
    (path / 'tests').mkdir()
    (path / 'README.md').write_text(README)
    (path / 'pricing.py').write_text(PRICING_BASE)
    (path / 'tests' / '__init__.py').write_text('')
    (path / 'tests' / 'test_pricing.py').write_text(TESTS)
    run(path, 'git', 'init', '-q', '-b', 'feat/123-bulk-discount')
    run(path, 'git', '-c', 'user.name=fixture', '-c', 'user.email=fixture@example.test',
        'add', '.')
    run(path, 'git', '-c', 'user.name=fixture', '-c', 'user.email=fixture@example.test',
        'commit', '-q', '-m', 'feat: order pricing with member and bulk discounts')
    (path / 'pricing.py').write_text(PRICING_CHANGED)


def catalog(skills):
    rows = []
    for skill in sorted(skills.glob('coco-*/SKILL.md')):
        text = skill.read_text()
        desc = re.search(r'^description: "(.*)"$', text, re.M).group(1)
        rows.append('- %s: %s' % (skill.parent.name, desc))
    return '\n'.join(rows)


def body(skills, name):
    text = (skills / name / 'SKILL.md').read_text()
    return text.split('---', 2)[2].lstrip('\n')


TEMPLATE = """You are acting as Claude Code, the coding agent, in a session whose working directory is {repo}. Answer exactly as you would to the user in that session, using your tools for any work you decide to do. The user's language is Korean.

Sandbox limits: work only inside {repo}, and read skill files only under {skills}. Do not touch any other path, do not contact any remote, and do not install anything.

The following skills are available in this session:
{catalog}
{history}
The user's newest message is a slash command, which Claude Code expanded as follows:

<command-name>/{name}</command-name>
Base directory for this skill: {skills}/{name}

{body}

When this turn is done, end with exactly two sections:
## Response
(the complete user-facing message you would send for this turn, verbatim)
## Actions
(every command you ran and every file you read or wrote, one per line, in order)
"""

DEBUG_HISTORY = """
Conversation so far:
User: pricing 테스트 돌렸더니 test_bulk_nonmember가 실패해. 기대값은 285인데 300이 나와. 방금 pricing.py 리팩터링한 뒤부터 그래.
Assistant: 확인해 보니 tests/test_pricing.py의 test_bulk_nonmember가 실패합니다(기대 285, 실제 300). pricing.py의 커밋되지 않은 리팩터링 이후부터 발생했습니다. 원인을 조사해 볼까요?
"""

CASES = {
    'a-review-bare': ('coco-review', ''),
    'b-debug-context': ('coco-debug', DEBUG_HISTORY),
    'c-askme-bare': ('coco-askme', ''),
    'd-push-bare': ('coco-push', ''),
    'e-build-bare': ('coco-build', ''),
    # Second round: merge joins push as a skill that runs directly; ship is the nearest non-exempt control.
    'f-merge-bare': ('coco-merge', ''),
    'g-ship-bare': ('coco-ship', ''),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, default=BASE,
                        help='folder holding snapshot/skills; repos/ and prompts/ are written here')
    parser.add_argument('cases', nargs='*', help='cases to build (default: all)')
    args = parser.parse_args()
    work = args.work.resolve()
    skills = work / 'snapshot' / 'skills'
    cat = catalog(skills)
    for case in args.cases or CASES:
        name, history = CASES[case]
        repo = work / 'repos' / case
        make_repo(repo)
        prompt = TEMPLATE.format(repo=repo, skills=skills, catalog=cat, history=history,
                                 name=name, body=body(skills, name))
        (work / 'prompts').mkdir(exist_ok=True)
        (work / 'prompts' / (case + '.md')).write_text(prompt)
        print(case, repo)


if __name__ == '__main__':
    main()
