import unittest
from discount import net_total

class DiscountTest(unittest.TestCase):
    def test_ten_percent(self):
        self.assertEqual(net_total(100, 10), 90)

    def test_no_discount(self):
        self.assertEqual(net_total(100, 0), 100)
