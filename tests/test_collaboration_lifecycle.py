"""Validate the private lifecycle oracle against public executable controls."""
import importlib.util
import json
from pathlib import Path
import shutil
import sqlite3
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'docs/evaluation/collaboration-value/lifecycle.py'
CONTROL = ROOT / 'tests/fixtures/collaboration_catalog_control.py'
spec = importlib.util.spec_from_file_location('collaboration_lifecycle', PATH)
lifecycle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lifecycle)


class LifecycleObserverTests(unittest.TestCase):
    def project(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        project = Path(temp.name) / 'catalog-project'
        lifecycle.prepare(project, 11)
        return project

    def control(self, project, profile, phase, fault=None):
        shutil.copyfile(CONTROL, project / 'catalog.py')
        (project / '_catalog_control.json').write_text(json.dumps({
            'profile': profile, 'phase': phase, 'fault': fault}))

    def test_original_seed_fails_the_real_import_milestone(self):
        project = self.project()
        report = lifecycle.verify(project, lifecycle.PROFILES[0], 'initial', milestone=True)
        self.assertFalse(report['passed'])
        self.assertFalse(report['checks'][0]['passed'])
        self.assertEqual(report['checks'][0]['id'], 'runnable_unique_import')

    def test_clean_reference_passes_every_phase_for_all_five_owner_profiles(self):
        for index, profile in enumerate(lifecycle.PROFILES):
            project = self.project()
            for phase in ('initial', 'changed', 'resumed'):
                with self.subTest(profile=index, phase=phase):
                    self.control(project, profile, phase)
                    report = lifecycle.verify(project, profile, phase)
                    self.assertTrue(report['passed'], report['checks'])
                    self.assertTrue(report['actions'])
                    self.assertTrue(all('catalog.py' in row['argv']
                                        for row in report['actions']))

    def test_wrong_identity_is_detected_for_fold_and_exact_profiles_then_restored(self):
        for index in (0, 1):
            with self.subTest(profile=index):
                project = self.project()
                profile = lifecycle.PROFILES[index]
                self.control(project, profile, 'initial', fault='identity')
                report = lifecycle.verify(project, profile, 'initial')
                failed = {row['id'] for row in report['checks'] if not row['passed']}
                self.assertIn('chosen_identity_and_file_collision', failed)
                self.control(project, profile, 'initial')
                self.assertTrue(lifecycle.verify(project, profile, 'initial')['passed'])

    def test_reapplying_an_old_batch_is_detected_and_clean_restore_passes(self):
        project = self.project()
        profile = lifecycle.PROFILES[2]
        self.control(project, profile, 'changed', fault='replay')
        report = lifecycle.verify(project, profile, 'changed')
        failed = {row['id'] for row in report['checks'] if not row['passed']}
        self.assertIn('old_replay_does_not_roll_back', failed)
        self.control(project, profile, 'changed')
        self.assertTrue(lifecycle.verify(project, profile, 'changed')['passed'])

    def test_actual_owner_data_loss_fails_even_when_external_probe_databases_pass(self):
        project = self.project()
        profile = lifecycle.PROFILES[0]
        self.control(project, profile, 'initial')
        connection = sqlite3.connect(project / 'store.sqlite')
        connection.execute('DELETE FROM catalog')
        connection.commit()
        connection.close()
        report = lifecycle.verify(project, profile, 'initial')
        failed = {row['id'] for row in report['checks'] if not row['passed']}
        self.assertEqual(failed, {'original_user_data_preserved'})

    def test_wrong_zero_policy_is_detected_in_both_directions_then_restored(self):
        for index in (0, 1):
            with self.subTest(profile=index):
                project = self.project()
                profile = lifecycle.PROFILES[index]
                self.control(project, profile, 'resumed', fault='summary')
                report = lifecycle.verify(project, profile, 'resumed')
                failed = {row['id'] for row in report['checks'] if not row['passed']}
                self.assertIn('summary_uses_agreed_rule', failed)
                self.control(project, profile, 'resumed')
                self.assertTrue(lifecycle.verify(project, profile, 'resumed')['passed'])


if __name__ == '__main__':
    unittest.main()
