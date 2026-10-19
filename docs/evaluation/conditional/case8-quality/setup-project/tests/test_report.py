import unittest
from src.report import report
class ReportTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(report([]), "empty")
