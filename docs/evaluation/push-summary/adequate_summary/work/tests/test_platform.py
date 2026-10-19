import unittest
from src.platform import default_timeout
class Platform(unittest.TestCase):
    def test_default_timeout(self):
        self.assertEqual(default_timeout(), 30)
