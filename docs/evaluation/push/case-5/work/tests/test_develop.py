import unittest
from app import greet

class DevelopTests(unittest.TestCase):
    def test_whitespace(self):
        self.assertNotIn(" Ada ", greet(" Ada "))
