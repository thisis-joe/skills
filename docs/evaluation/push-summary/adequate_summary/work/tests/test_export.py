import csv
import io
import unittest
from src.exporter import export_csv

class ExportBehavior(unittest.TestCase):
    def test_quoted_unicode_round_trip(self):
        rows = [["홍길동", 'hello, "world"'], ["Ada", "line1\nline2"]]
        self.assertEqual(list(csv.reader(io.StringIO(export_csv(rows)))), [["name", "note"], *rows])
    def test_empty_output_still_has_header(self):
        self.assertEqual(list(csv.reader(io.StringIO(export_csv([])))), [["name", "note"]])
