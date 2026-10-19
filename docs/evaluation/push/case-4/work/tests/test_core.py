import unittest
from app import greet

class CoreTests(unittest.TestCase):
    def test_greeting(self):
        self.assertTrue(greet("Ada").startswith("Hello, Ada"))
