"""Structural and installed-artifact guards; agent behavior is evaluated separately."""
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class StagedWorkflowTests(unittest.TestCase):
    def test_introductory_map_is_exactly_ten_registered_skills(self):
        text = (ROOT / 'skills/_coco-shared/workflow.md').read_text()
        table = text.split('## Introductory path\n', 1)[1].split('\nInstall all skills.', 1)[0]
        names = re.findall(r'`(coco-[a-z]+)`', table)
        self.assertEqual(len(names), 10)
        self.assertEqual(len(set(names)), 10)
        registered = json.loads((ROOT / 'coco.json').read_text())['skills']
        self.assertTrue(set(names) < set(registered))
        for name in names:
            self.assertTrue((ROOT / 'skills' / name / 'SKILL.md').is_file())

    def test_actual_install_contains_policy_and_preserves_unrelated_file(self):
        with tempfile.TemporaryDirectory() as folder:
            dest = Path(folder) / 'skills'
            dest.mkdir()
            sentinel = dest / 'user-note.txt'
            sentinel.write_bytes(b'keep user work\n')
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/install.py'),
                                     '--dest', str(dest)], capture_output=True, text=True,
                                    stdin=subprocess.DEVNULL)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual((dest / '_coco-shared/workflow.md').read_bytes(),
                             (ROOT / 'skills/_coco-shared/workflow.md').read_bytes())
            self.assertEqual(sentinel.read_bytes(), b'keep user work\n')
            check = subprocess.run([sys.executable, str(ROOT / 'scripts/validate.py'),
                                    '--installed', str(dest)], capture_output=True, text=True)
            self.assertEqual(check.returncode, 0, check.stdout + check.stderr)


if __name__ == '__main__':
    unittest.main()
