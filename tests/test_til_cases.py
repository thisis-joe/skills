"""Check real TIL workspaces with the standalone troubleshooting case checker."""
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

from test_til_notes import CHECKER as NOTE_CHECKER, EXAMPLE, SKILL, documented_blocks


CHECKER = SKILL / 'tools/check_cases.py'
FORMAT = SKILL / 'references/case-template.md'
CASE_PATH = 'cases/jenkins-queue.md'
CASE_ENTRY = '- [Jenkins 대기 지연](cases/jenkins-queue.md) — 실행기 점유 확인\n'
INDEX = '# TIL\n\n## 문제 해결 사례\n\n' + CASE_ENTRY
SOURCE_LINE = 'sources: [checkout job build 71, checkout job build 72]'
CASE = f"""---
title: Jenkins 대기 지연
created: 2026-11-06
updated: 2026-11-06
{SOURCE_LINE}
---

# Jenkins 대기 지연

## 증상과 성공 기준

빌드 71은 첫 단계 전 10분 대기했다. 다음 실행의 대기가 1분 미만이면 복구로 본다.

## 진단 순서

빌드 71의 대기 로그와 실행기 화면을 대조해 모든 실행기가 점유된 것을 확인했다.

## 다음에 따라 할 절차

읽기 전용 확인. Jenkins에서 잡과 빌드 번호를 바꿔 대기 로그를 찾는다.
첫 단계 전이 길면 실행기 점유를 확인한다. 단계 자체가 길면 단계 로그를 확인한다.

## 수정과 재검증

예약된 실행기를 복구했다. 빌드 72는 같은 잡에서 20초 대기했고, 부하는 기록되지 않았다.
"""


class TilCaseTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name) / '학습 공간'
        (self.root / 'cases').mkdir(parents=True)
        [template] = re.findall(r'^\x60{4}markdown\n(.*?)^\x60{4}$',
                                FORMAT.read_text(encoding='utf-8'), re.S | re.M)
        labels = ['Symptoms and success criteria', 'Diagnostic sequence',
                  'Procedure for next time', 'Fix and revalidation']
        translated = ['증상과 성공 기준', '진단 순서', '다음에 따라 할 절차', '수정과 재검증']
        for english, korean in zip(labels, translated):
            template = template.replace(f'## {english}\n', f'## {korean}\n')
        self.write('CASE_TEMPLATE.md', template)
        self.write(CASE_PATH, CASE)
        self.write('INDEX.md', INDEX)

    def write(self, path, text):
        (self.root / path).write_text(text, encoding='utf-8')

    def check(self, expected=0, checker=CHECKER):
        result = subprocess.run([sys.executable, str(checker), str(self.root)],
                                capture_output=True, encoding='utf-8')
        output = result.stdout + result.stderr
        self.assertEqual(result.returncode, expected, output)
        return output

    def test_case_only_workspace_needs_no_concept_storage(self):
        before = {path.relative_to(self.root): (path.read_bytes(), path.stat().st_mtime_ns)
                  for path in self.root.rglob('*.md')}
        self.assertIn('OK: 1 troubleshooting case', self.check())
        self.assertFalse((self.root / 'TEMPLATE.md').exists())
        self.assertFalse((self.root / 'notes').exists())
        after = {path.relative_to(self.root): (path.read_bytes(), path.stat().st_mtime_ns)
                 for path in self.root.rglob('*.md')}
        self.assertEqual(before, after)

    def test_mixed_workspace_passes_both_checkers(self):
        (self.root / 'notes').mkdir()
        [template] = documented_blocks()
        self.write('TEMPLATE.md', template)
        self.write('notes/atomic-replace.md', EXAMPLE.read_text(encoding='utf-8'))
        self.write('INDEX.md', INDEX + '\n## Python\n\n'
                   '- [Atomic replace with os.replace](notes/atomic-replace.md) — safe swap\n')
        self.assertIn('OK: 1 troubleshooting case', self.check())
        self.assertIn('OK: 1 note (learning 0, understood 1, review 0)',
                      self.check(checker=NOTE_CHECKER))

    def test_case_requires_actual_evidence_pointers(self):
        for sources in ('sources: []', 'sources: [<build or artifact reference>]'):
            with self.subTest(sources=sources):
                self.write(CASE_PATH, CASE.replace(SOURCE_LINE, sources))
                self.assertIn('sources must list actual evidence pointers', self.check(1))

    def test_case_rejects_reordered_or_empty_sections(self):
        self.write(CASE_PATH, CASE.replace('## 진단 순서', '## 수정과 재검증')
                   .replace('## 수정과 재검증\n\n예약', '## 진단 순서\n\n예약'))
        self.assertIn('case sections must be exactly, in order', self.check(1))
        self.write(CASE_PATH, CASE.split('예약된 실행기', 1)[0])
        self.assertIn('case section is empty: 수정과 재검증', self.check(1))

    def test_index_requires_one_real_entry_in_case_section(self):
        indexes = [
            (INDEX + CASE_ENTRY, 'is listed 2 times'),
            (INDEX.replace(CASE_ENTRY, '') + '\n## Other\n\n' + CASE_ENTRY, 'only under'),
            (INDEX.replace(CASE_ENTRY, '```markdown\n' + CASE_ENTRY + '```\n'), 'is listed 0 times'),
            (INDEX.replace('jenkins-queue.md', 'missing.md'), 'existing cases/<slug>.md'),
        ]
        for index, problem in indexes:
            with self.subTest(problem=problem):
                self.write('INDEX.md', index)
                self.assertIn(problem, self.check(1))
