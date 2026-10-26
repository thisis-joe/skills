"""The comparative observer must detect wrong actual outputs, not just file names."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import sys

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'docs/evaluation/staged-development/scenarios.py'
spec = importlib.util.spec_from_file_location('staged_scenarios', PATH)
scenarios = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scenarios)
sys.path.insert(0, str(PATH.parent))
from run import needs_followup


class StagedEvaluationTests(unittest.TestCase):
    def test_resolved_commentary_does_not_create_a_fake_user_turn(self):
        self.assertFalse(needs_followup(['Implementation complete; review pending.',
                                        'Formal review and execution checks completed.']))
        self.assertTrue(needs_followup(['Specification saved.',
                                       'Which option would you like next?']))
        self.assertFalse(needs_followup(['Browser verification pending; no runner is available.']))
        self.assertTrue(needs_followup(['Formal review is pending.']))
        self.assertFalse(needs_followup(['Formal review completed. No review pending.']))

    def project(self, case):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name) / 'project'
        scenarios.prepare(root, case)
        return root

    def test_copy_observer_checks_exact_result_and_preservation(self):
        root = self.project('copy')
        self.assertFalse(scenarios.verify(root, 'copy')['functional_pass'])
        page = root / 'index.html'
        original = page.read_text()
        page.write_text(original.replace('>Save<', '>Save changes<'))
        before = page.read_bytes()
        self.assertTrue(scenarios.verify(root, 'copy')['functional_pass'])
        page.write_text(page.read_text().replace('Saved records', 'lost content'))
        self.assertFalse(scenarios.verify(root, 'copy')['functional_pass'])
        page.write_bytes(before)
        self.assertTrue(scenarios.verify(root, 'copy')['functional_pass'])

    def test_pagination_observer_rejects_real_broken_cli(self):
        root = self.project('pagination')
        report = scenarios.verify(root, 'pagination')
        self.assertFalse(report['functional_pass'])
        self.assertTrue(any(row['argv'][1]=='catalog.py' for row in report['actions']))
        self.assertFalse(next(row for row in report['assertions']
                              if row['check']=='full nonduplicated traversal')['passed'])

    def test_runtime_gap_never_becomes_executed_from_html_presence(self):
        root = self.project('runtime-gap')
        page = root / 'index.html'
        page.write_text(page.read_text()+'<script>document.querySelector("button").onclick=()=>{};</script>')
        report = scenarios.verify(root, 'runtime-gap')
        self.assertTrue(report['functional_pass'])
        self.assertEqual(report['required_runtime'], 'unavailable: actual browser')
        self.assertIn('do not prove browser behavior', report['limits'])


if __name__ == '__main__':
    unittest.main()
