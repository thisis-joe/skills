import unittest
from ledger import total
class LedgerTest(unittest.TestCase):
    def test_total(self):
        self.assertEqual(total([3, 4]), 7)
