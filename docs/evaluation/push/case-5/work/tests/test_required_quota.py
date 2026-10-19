import unittest
from quota import allowed

class RequiredQuotaTests(unittest.TestCase):
    def test_zero_contract(self):
        self.assertTrue(allowed(0), "Required quota contract remains unresolved")
