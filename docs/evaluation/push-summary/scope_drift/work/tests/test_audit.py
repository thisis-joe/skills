import unittest
from src.audit import event_name
class Audit(unittest.TestCase):
    def test_rotation_audit_contract(self):
        self.assertEqual(event_name(), "refresh-token-rotated")
