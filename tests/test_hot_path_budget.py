"""Bound the guidance push, merge and ship always read before acting.

A regrowth guard for the latency audit in docs/evaluation/latency/, not evidence
of agent quality. Characters are counted after normalizing CRLF so a Windows
checkout measures the same text.
"""
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = 'skills/_coco-shared/contracts.md'
HOT_PATHS = {
    'push': ['skills/coco-push/SKILL.md', CONTRACT, 'skills/coco-push/references/sync-and-push.md',
             'skills/coco-push/references/pull-request.md'],
    'merge': ['skills/coco-merge/SKILL.md', CONTRACT, 'skills/coco-merge/references/forge-merge.md'],
    'ship': ['skills/coco-ship/SKILL.md', CONTRACT],
}
# Measured after the first latency changes plus 2%; raising one needs a decisions.md row.
MAX_CHARACTERS = {'push': 35500, 'merge': 26800, 'ship': 12000}


def characters(paths, root=ROOT):
    """A missing file raises instead of counting as empty."""
    return sum(len((Path(root) / path).read_bytes().decode('utf-8').replace('\r\n', '\n'))
               for path in paths)


class HotPathBudgetTests(unittest.TestCase):
    def test_always_read_guidance_stays_within_budget(self):
        for name, paths in HOT_PATHS.items():
            with self.subTest(path=name):
                self.assertLessEqual(characters(paths), MAX_CHARACTERS[name])

    def test_crlf_checkout_counts_the_same(self):
        with tempfile.TemporaryDirectory() as scratch:
            source = (ROOT / CONTRACT).read_bytes()
            copy = Path(scratch) / CONTRACT
            copy.parent.mkdir(parents=True)
            copy.write_bytes(source.replace(b'\r\n', b'\n').replace(b'\n', b'\r\n'))
            self.assertEqual(characters([CONTRACT], scratch), characters([CONTRACT]))

    def test_missing_file_fails(self):
        with tempfile.TemporaryDirectory() as scratch:
            with self.assertRaises(FileNotFoundError):
                characters([CONTRACT], scratch)


if __name__ == '__main__':
    unittest.main()
