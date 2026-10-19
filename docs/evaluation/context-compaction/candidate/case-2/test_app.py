import subprocess
import sys
import unittest
class CliTests(unittest.TestCase):
    def test_double(self):
        result = subprocess.run([sys.executable, 'app.py', '--double', '3'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), '6')
