import unittest
from pricing import total

class BulkTests(unittest.TestCase):
    def test_bulk_nonmember(self):
        self.assertEqual(total(100, 3), 285)
