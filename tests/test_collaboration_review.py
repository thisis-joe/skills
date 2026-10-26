"""The review observer exercises reachable defects and a repaired public CLI."""
import importlib.util
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'docs/evaluation/collaboration-value/review_case.py'


class ReviewFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('collaboration_review', PATH)
        cls.fixture = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.fixture)

    def project(self, seed=1):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        project = Path(temp.name) / 'billing-project'
        metadata = self.fixture.prepare(project, seed)
        return project, metadata

    def test_seed_is_green_but_observer_reproduces_three_root_defects(self):
        project, metadata = self.project()
        visible = subprocess.run(['python3', '-m', 'unittest', 'discover', '-v'],
                                 cwd=project, text=True, capture_output=True)
        self.assertEqual(visible.returncode, 0, visible.stderr)
        report = self.fixture.verify_defects(project)
        self.assertFalse(report['functional_pass'])
        self.assertEqual(report['defects'], {
            'cache_authorization': True, 'payload_replay': True,
            'rejected_refund_mutation': True})
        failed = {row['id'] for row in report['checks'] if not row['passed']}
        self.assertEqual(failed, {'warmed_cache_authorization', 'replay_amount',
                                 'replay_invoice', 'rejected_refund_no_mutation'})
        self.assertTrue(report['actions'])
        self.assertTrue(all(row['exit'] == 0 for row in report['actions']))
        self.assertGreater(metadata['source_lines'], 150)
        self.assertLess(metadata['source_lines'], 251)

    def test_repaired_control_passes_identical_public_checks_and_preserves_notes(self):
        project, _ = self.project(4)
        self.fixture.repair(project)
        report = self.fixture.verify_defects(project)
        self.assertTrue(report['functional_pass'], report['checks'])
        self.assertFalse(any(report['defects'].values()))
        self.assertEqual((project / 'personal-notes.txt').read_text(),
                         self.fixture.NOTES)
        tracked = subprocess.check_output(['git', 'ls-files', 'personal-notes.txt'],
                                          cwd=project, text=True)
        self.assertEqual(tracked, '')

    def test_base_is_valid_and_proposed_patch_is_a_real_git_diff(self):
        project, metadata = self.project(3)
        patch = subprocess.check_output(['git', 'diff', metadata['base_commit'],
                                         metadata['patch_commit']], cwd=project,
                                        text=True)
        self.assertIn('service.py', patch)
        self.assertIn('refund', patch)
        subprocess.run(['git', 'show', metadata['base_commit'] + ':service.py'],
                       cwd=project, check=True, capture_output=True)
        base = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, base)
        for name in ('billing.py', 'service.py', 'storage.py', 'seed.json'):
            content = subprocess.check_output(
                ['git', 'show', metadata['base_commit'] + ':' + name], cwd=project)
            (base / name).write_bytes(content)
        action = self.fixture.run_cli(base, base / 'base.db', [
            {'op': 'invoice', 'tenant': 'north', 'invoice': 'inv-a'},
            {'op': 'invoice', 'tenant': 'south', 'invoice': 'inv-a'}])
        self.assertTrue(action['responses'][0]['ok'])
        self.assertFalse(action['responses'][1]['ok'])

    def test_paired_projects_are_identical_without_hidden_observer_or_hints(self):
        left, left_meta = self.project(5)
        right, right_meta = self.project(5)
        self.assertEqual(left_meta['base_commit'], right_meta['base_commit'])
        self.assertEqual(left_meta['patch_commit'], right_meta['patch_commit'])
        for name in ('billing.py', 'service.py', 'storage.py', 'seed.json',
                     'README.md', 'test_billing.py'):
            self.assertEqual((left / name).read_bytes(), (right / name).read_bytes())
        files = {path.name for path in left.iterdir()}
        self.assertNotIn('review_case.py', files)
        self.assertNotIn('defects.json', files)
        self.assertNotIn('seeded', self.fixture.PROMPT.lower())
        self.assertNotIn('three', self.fixture.PROMPT.lower())
        self.assertNotIn('warm', self.fixture.PROMPT.lower())


if __name__ == '__main__':
    unittest.main()
