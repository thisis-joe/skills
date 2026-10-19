import unittest
from src.tokens import expired, TokenFamily

class TokenBehavior(unittest.TestCase):
    def test_expiry_boundary(self):
        self.assertFalse(expired(9, 10))
        self.assertTrue(expired(10, 10))
    def test_rotation_returns_fresh_token(self):
        family = TokenFamily()
        next_token = family.rotate("token-0")
        self.assertNotEqual(next_token, "token-0")
        self.assertNotEqual(family.rotate(next_token), next_token)
    def test_reuse_revokes_family(self):
        family = TokenFamily()
        next_token = family.rotate("token-0")
        with self.assertRaisesRegex(ValueError, "reused"):
            family.rotate("token-0")
        with self.assertRaisesRegex(ValueError, "invalid"):
            family.rotate(next_token)
