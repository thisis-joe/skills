import unittest
from app import double

class DoubleTests(unittest.TestCase):
    def test_positive_and_negative(self):
        self.assertEqual(double(3), 6)
        self.assertEqual(double(-4), -8)
