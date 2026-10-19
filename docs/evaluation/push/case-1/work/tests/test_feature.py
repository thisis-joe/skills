import unittest
from app import greet

class FeatureTests(unittest.TestCase):
    def test_exclamation(self):
        self.assertTrue(greet("Ada").endswith("!"))
