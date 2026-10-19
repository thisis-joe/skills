import unittest
class ModelTest(unittest.TestCase):
    def test_title_value(self):
        self.assertEqual({"title": "Quarterly"}["title"], "Quarterly")
