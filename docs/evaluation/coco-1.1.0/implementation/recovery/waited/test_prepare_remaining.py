"""Offline restoration and explicit-run guards; native models are never invoked."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('remaining', HERE/'prepare_remaining.py')
helper = importlib.util.module_from_spec(spec); spec.loader.exec_module(helper)


class RemainingTests(unittest.TestCase):
    def test_real_archive_offline_restore_and_run_guards(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder)/'prepared'
            with patch.object(helper.subprocess, 'run', side_effect=AssertionError('No subprocess during prepare')):
                receipt = helper.prepare(output, HERE/'evidence/budget900-first-native.tar.gz', HERE/'evidence/budget900-first-native-manifest.json')
            runtime = output/'runtime'
            control = helper.read(runtime/'control.json')
            self.assertEqual(len(control['trials']), 11)
            self.assertNotIn(helper.FIRST_ID, receipt['pending_order'])
            self.assertFalse((runtime/'STOP').exists())
            self.assertTrue((output/'source-original'/'STOP').exists())
            self.assertFalse(list((runtime/'records').rglob('turn-*.json')))
            self.assertEqual(len(control['hashes']), 22)
            with patch.object(helper.subprocess, 'run') as version, patch.object(helper.subprocess, 'call') as launch:
                version.return_value.stdout = 'codex-cli changed'
                with self.assertRaisesRegex(ValueError, 'CLI version changed'):
                    helper.run_explicit(output)
                launch.assert_not_called()
            project = Path(control['trials'][0]['project'])
            (project/'unexpected.txt').write_text('tampered')
            with patch.object(helper.subprocess, 'run') as version, patch.object(helper.subprocess, 'call') as launch:
                with self.assertRaisesRegex(ValueError, 'Prepared state changed'):
                    helper.run_explicit(output)
                version.assert_not_called(); launch.assert_not_called()
            with self.assertRaises(FileExistsError):
                helper.prepare(output, HERE/'evidence/budget900-first-native.tar.gz', HERE/'evidence/budget900-first-native-manifest.json')

    def test_archive_tamper_rejected_before_extract(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); archive = root/'bad.tar.gz'; archive.write_bytes(b'bad')
            with self.assertRaisesRegex(ValueError, 'archive hash differs'):
                helper.extract_checked(archive, HERE/'evidence/budget900-first-native-manifest.json', root/'out')
            self.assertFalse((root/'out').exists())

    def test_manifest_tamper_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); value = helper.read(HERE/'evidence/budget900-first-native-manifest.json')
            first = next(iter(value['members'])); value['members'][first]['mode'] ^= 0o100
            manifest = root/'manifest.json'; manifest.write_text(json.dumps(value))
            with self.assertRaisesRegex(ValueError, 'byte/mode mismatch'):
                helper.extract_checked(HERE/'evidence/budget900-first-native.tar.gz', manifest, root/'out')


if __name__ == '__main__':
    unittest.main()
