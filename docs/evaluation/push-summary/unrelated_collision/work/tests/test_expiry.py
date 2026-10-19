import unittest
from src.tokens import expired
class Expiry(unittest.TestCase):
    def test_expired(self):
        self.assertTrue(expired(10, 10))
