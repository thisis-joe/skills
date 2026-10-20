"""Run the coco-learn checker on real workspaces, including translated labels."""
from pathlib import Path
import re
import runpy
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/coco-learn'
CHECKER = SKILL / 'tools/check_notes.py'
FORMAT = SKILL / 'references/note-template.md'
EXAMPLE = SKILL / 'references/example-note.md'
LABELS = ('Key points', 'Example', 'Pitfalls', 'Self-check', 'Related')
KOREAN = ('핵심', '예시', '함정', '셀프 체크', '관련')


def documented_blocks():
    text = FORMAT.read_text(encoding='utf-8')
    return re.findall(r'^````markdown\n(.*?)^````$', text, re.S | re.M)


def korean_note(title, related, status='learning'):
    return f"""---
title: {title}
tags: [python, 파일시스템]
status: {status}
created: 2026-10-01
updated: 2026-10-20
sources: [skills/scripts/install.py:79]
---

# {title}

> 임시 위치에 다 만든 뒤 한 번에 바꾸면 읽는 쪽은 반쯤 만든 결과를 보지 않는다.

## 핵심

- 새 내용은 대상과 같은 폴더의 임시 위치에 먼저 쓴다.
- `os.replace`는 같은 파일시스템 안에서 원자적으로 교체한다.

## 예시

`skills/scripts/install.py:79` `install()`은 스테이징 폴더를 채운 뒤 폴더 단위로 교체한다.

## 함정

- 원자성은 내구성이 아니다. 전원이 나가도 남아야 하면 `fsync`가 필요하다.

## 셀프 체크

<details><summary>임시 파일을 왜 대상 옆에 만드나?</summary>다른 파일시스템이면 교체가 실패할 수 있다.</details>

## 관련

- [{related}]({related}.md)
"""


class LearnNoteTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name) / '학습 공간'
        (self.root / 'notes').mkdir(parents=True)
        template = documented_blocks()[0]
        for english, korean in zip(LABELS, KOREAN):
            template = template.replace('## ' + english + '\n', '## ' + korean + '\n')
        self.write('TEMPLATE.md', template)
        self.write('notes/atomic-replace.md', korean_note('원자적 파일 교체', 'staging-install'))
        self.write('notes/staging-install.md',
                   korean_note('스테이징 설치', 'atomic-replace', status='review'))
        self.write('INDEX.md', '# 학습 노트\n\n## 파이썬\n\n'
                   '- [원자적 파일 교체](notes/atomic-replace.md) — 반쯤 쓴 파일 방지\n'
                   '- [스테이징 설치](notes/staging-install.md) — 폴더 단위 교체\n')

    def write(self, rel, text):
        (self.root / rel).write_text(text, encoding='utf-8')

    def edit(self, rel, old, new):
        path = self.root / rel
        text = path.read_text(encoding='utf-8')
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1), encoding='utf-8')

    def check(self, target=None, expect=0, *args):
        result = subprocess.run(
            [sys.executable, '-B', str(CHECKER), str(target or self.root), *args],
            capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, expect, result.stdout + result.stderr)
        return result.stdout + result.stderr

    def test_documented_template_and_example_pass_together(self):
        [template] = documented_blocks()
        example = EXAMPLE.read_text(encoding='utf-8')
        self.write('TEMPLATE.md', template)
        for note in (self.root / 'notes').iterdir():
            note.unlink()
        self.write('notes/atomic-replace-os.md', example)
        self.write('INDEX.md', '# Learning\n\n## Python\n\n'
                   '- [Atomic replace with os.replace](notes/atomic-replace-os.md) — safe swap\n')
        self.assertIn('OK: 1 note (learning 0, understood 1, review 0)', self.check())

    def test_translated_labels_pass_and_list_notes_to_reread(self):
        output = self.check()
        self.assertIn('OK: 2 notes (learning 1, understood 0, review 1)', output)
        self.assertIn('Reread next: staging-install.md, atomic-replace.md', output)
        self.assertIn('OK: 1 note', self.check(self.root / 'notes/atomic-replace.md'))

    def test_renamed_reordered_or_extra_sections_fail(self):
        self.edit('notes/atomic-replace.md', '## 함정', '## 주의')
        self.assertIn('sections must be exactly, in order: 핵심 / 예시 / 함정 / 셀프 체크 / 관련',
                      self.check(expect=1))
        self.edit('notes/atomic-replace.md', '## 주의', '## 함정')
        self.edit('notes/atomic-replace.md', '## 관련', '### 더 보기\n\n## 관련')
        self.assertIn('only the title and the template sections may be headings',
                      self.check(expect=1))

    def test_budget_violations_point_to_the_offending_part(self):
        self.edit('notes/atomic-replace.md', '- 새 내용은', '- 하나\n- 둘\n- 셋\n- 넷\n- 새 내용은')
        self.assertIn('section has 6 bullets; expected 2-5', self.check(expect=1))
        self.edit('notes/atomic-replace.md', '- 하나\n- 둘\n- 셋\n- 넷\n', '')
        self.edit('notes/atomic-replace.md', '## 예시\n', '## 예시\n\n```python\n' +
                  'pass\n' * 16 + '```\n')
        self.assertIn('example code has 16 lines; limit is 15', self.check(expect=1))
        self.edit('notes/atomic-replace.md', 'pass\n' * 16, 'pass\n')
        self.edit('notes/atomic-replace.md', '- 원자성은', '- ' + '가' * 161 + '\n- 원자성은')
        self.assertIn('bullet has 161 characters; limit is 160', self.check(expect=1))

    def test_long_note_must_be_split(self):
        self.edit('notes/atomic-replace.md', '## 예시\n', '## 예시\n' + '설명 문장.\n\n' * 20)
        self.assertIn('lines after frontmatter; limit is 60. Split the note by concept',
                      self.check(expect=1))

    def test_summary_status_dates_and_links_are_checked(self):
        self.edit('notes/atomic-replace.md', 'status: learning', 'status: done')
        self.edit('notes/atomic-replace.md', 'updated: 2026-10-20', 'updated: 2026-09-01')
        self.edit('notes/atomic-replace.md', '(staging-install.md)', '(missing.md)')
        self.edit('notes/atomic-replace.md', '반쯤 만든 결과를 보지 않는다.',
                  '반쯤 만든 결과를 보지 않는다.\n> 두 번째 줄')
        output = self.check(expect=1)
        for message in ('status must be one of: learning, understood, review',
                        'updated is earlier than created', 'broken link: missing.md',
                        'put exactly one "> summary" line under the title'):
            self.assertIn(message, output)

    def test_index_lists_each_note_once_and_titles_stay_unique(self):
        self.edit('INDEX.md', '- [스테이징 설치](notes/staging-install.md) — 폴더 단위 교체\n', '')
        self.assertIn('notes/staging-install.md is listed 0 times', self.check(expect=1))
        self.edit('INDEX.md', '## 파이썬\n', '## 파이썬\n\n- [다시](notes/atomic-replace.md) — 중복\n'
                  '- [스테이징 설치](notes/staging-install.md) — 폴더 단위 교체\n')
        self.assertIn('notes/atomic-replace.md is listed 2 times', self.check(expect=1))
        self.edit('INDEX.md', '- [다시](notes/atomic-replace.md) — 중복\n', '')
        self.write('notes/atomic-replace-copy.md', korean_note('원자적 파일 교체', 'atomic-replace'))
        self.write('INDEX.md', (self.root / 'INDEX.md').read_text(encoding='utf-8') +
                   '- [사본](notes/atomic-replace-copy.md) — 사본\n')
        self.assertIn('keep one note per concept', self.check(expect=1))

    def test_title_ending_in_hash_is_not_a_closing_sequence(self):
        self.edit('notes/atomic-replace.md', 'title: 원자적 파일 교체', 'title: C# 원자적 교체')
        self.edit('notes/atomic-replace.md', '# 원자적 파일 교체', '# C# 원자적 교체')
        self.edit('INDEX.md', '[원자적 파일 교체]', '[C# 원자적 교체]')
        self.assertIn('OK: 2 notes', self.check())

    def test_missing_or_malformed_template_is_a_usage_error(self):
        self.edit('TEMPLATE.md', '## 관련\n', '')
        self.assertIn('template needs exactly 5 level-two sections, found 4',
                      self.check(expect=2))
        (self.root / 'TEMPLATE.md').unlink()
        self.assertIn('missing TEMPLATE.md', self.check(expect=2))

    def test_documented_limits_match_the_checker(self):
        limits = runpy.run_path(str(CHECKER))
        text = FORMAT.read_text(encoding='utf-8')
        self.assertIn(f"| 1 line, {limits['MAX_SUMMARY_CHARS']} characters |", text)
        self.assertEqual(text.count(f"{limits['MAX_ITEM_CHARS']} characters each"), 2)
        self.assertIn(f"| 1 code block, {limits['MAX_CODE_LINES']} code lines |", text)
        self.assertIn(f"| {limits['MAX_BODY_LINES']} lines |", text)
        sections = [f'{low}–{high}' for kind, low, high in limits['SECTIONS']
                    if kind != 'example']
        for expected in sections:
            self.assertIn(expected, text)

    def test_active_skills_route_learning_and_documents_separately(self):
        skills = ROOT / 'skills'
        stale = [str(path.relative_to(skills)) for path in skills.rglob('*.md')
                 if 'coco-document' in path.read_text(encoding='utf-8')
                 or 'document.md' in path.read_text(encoding='utf-8')]
        self.assertEqual(stale, [])
        learn = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('(references/note-template.md)', learn)
        self.assertIn('(tools/check_notes.py)', learn)
        self.assertIn('`coco-docs`', learn)
        docs = (skills / 'coco-docs/SKILL.md').read_text(encoding='utf-8')
        self.assertIn('`coco-learn`', docs)


if __name__ == '__main__':
    unittest.main()
