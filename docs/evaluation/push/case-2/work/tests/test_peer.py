import unittest
from peer import peer_enabled

class PeerTests(unittest.TestCase):
    def test_peer(self):
        self.assertTrue(peer_enabled())
