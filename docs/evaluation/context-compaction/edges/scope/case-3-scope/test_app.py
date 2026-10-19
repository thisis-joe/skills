import subprocess
import sys
import unittest


class CliTests(unittest.TestCase):
    def test_double_positive(self):
        result = subprocess.run([sys.executable, 'app.py', '--double', '3'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '6\n')


if __name__ == '__main__':
    unittest.main()
