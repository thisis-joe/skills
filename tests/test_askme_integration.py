"""Installation, reachability and opening-cost guards; not proof of LLM behavior."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from install import install
from package_utils import validate_installed


class AskmeIntegrationTests(unittest.TestCase):
    def test_installed_alias_reaches_single_owner_and_preserves_til(self):
        with tempfile.TemporaryDirectory() as td:
            dest = Path(td) / 'skills'
            foreign = dest / 'other-skill/SKILL.md'
            foreign.parent.mkdir(parents=True)
            foreign.write_text('unrelated user skill')
            result = install(ROOT, dest)
            self.assertEqual(result['status'], 'installed')
            info = validate_installed(dest)
            self.assertIn('coco-research', info['package']['skills'])
            self.assertIn('coco-askme', info['package']['skills'])
            alias = (dest / 'coco-research/SKILL.md').read_text()
            self.assertIn('(../coco-askme/SKILL.md)', alias)
            self.assertNotIn('## Procedure', alias)
            owner = (dest / 'coco-askme/SKILL.md').read_text()
            for ref in ('references/quiz.md', '../_coco-shared/advanced/research.md'):
                self.assertIn('(' + ref + ')', owner)
                self.assertTrue((dest / 'coco-askme' / ref).is_file())
            for source in (ROOT / 'skills/coco-til').rglob('*'):
                if source.is_file() and '__pycache__' not in source.parts:
                    relative = source.relative_to(ROOT / 'skills')
                    self.assertEqual(source.read_bytes(), (dest / relative).read_bytes())
            self.assertEqual(foreign.read_text(), 'unrelated user skill')
            before = (dest / '.coco-install.json').read_bytes()
            self.assertEqual(install(ROOT, dest)['status'], 'unchanged')
            self.assertEqual(before, (dest / '.coco-install.json').read_bytes())

    def test_opening_instruction_budget_and_deferred_quiz(self):
        # Prior askme entry was 6052 bytes at the approved TIL base. This bounds
        # instruction size only; actual token use and tool selection need runtime evidence.
        owner = (ROOT / 'skills/coco-askme/SKILL.md').read_bytes()
        self.assertLessEqual(len(owner), 6052)
        alias = (ROOT / 'skills/coco-research/SKILL.md').read_bytes()
        self.assertLessEqual(len(alias), 700)
        text = owner.decode()
        opening = text.split('## Topic orientation (wide)', 1)[1].split('## Evidence gathering', 1)[0]
        self.assertIn('at most two already identified session-linked sources', opening)
        self.assertIn('120 lines combined', opening)
        self.assertIn('no content-discovery calls', opening)
        self.assertIn('Whenever the menu relies on compressed or handoff context', opening)
        self.assertIn('even without recovery', opening)
        self.assertNotIn('](references/', opening)
        quiz = (ROOT / 'skills/coco-askme/references/quiz.md').read_text()
        self.assertIn('Never reveal the answer', quiz)
        self.assertIn('then stop and wait', quiz)

    def test_frozen_sources_and_research_ownership(self):
        coverage = json.loads((ROOT / 'sources/coverage.json').read_text())
        expected = {('matt', 'skills/engineering/research/SKILL.md'),
                    ('addy', 'skills/source-driven-development/SKILL.md'),
                    ('pstack', 'pstack/skills/how/SKILL.md'),
                    ('pstack', 'pstack/skills/why/SKILL.md')}
        rows = [r for r in coverage['entries'] if (r['author'], r['path']) in expected]
        self.assertEqual(len(rows), 4)
        for row in rows:
            self.assertEqual(row['family'], 'askme')
            self.assertIn('skills/coco-askme/SKILL.md', row['implemented_references'])
            self.assertIn('skills/_coco-shared/advanced/research.md', row['implemented_references'])
            self.assertTrue(row['essential_rules'])


if __name__ == '__main__':
    unittest.main()
