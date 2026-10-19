import subprocess
import sys
import unittest

class GreetTest(unittest.TestCase):
    def test_normal_cli(self):
        result = subprocess.run([sys.executable, "greet.py", "Ada"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "Hello, Ada.\n")

    def test_excited_cli(self):
        result = subprocess.run([sys.executable, "greet.py", "Ada", "--excited"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "Hello, Ada!\n")
