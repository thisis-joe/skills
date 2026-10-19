import unittest
from pricing import total

class PricingTests(unittest.TestCase):
    def test_regular(self):
        self.assertEqual(total(100, 1), 100)

    def test_member(self):
        self.assertEqual(total(100, 1, member=True), 90)
