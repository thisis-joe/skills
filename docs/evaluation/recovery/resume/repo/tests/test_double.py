import subprocess
import sys
import unittest
class DoubleTest(unittest.TestCase):
    def test_double(self):
        p=subprocess.run([sys.executable,"double.py","6"],capture_output=True,text=True)
        self.assertEqual(p.returncode,0)
        self.assertEqual(p.stdout,"12\n")
