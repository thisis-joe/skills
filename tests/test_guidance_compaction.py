"""Bound loading overhead; structural checks are not agent-quality evidence."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from test_context_loading import BASELINE, ROOT, inspect_context_loading, split_sections


COMPACTION_BASELINE = ROOT / 'tests/fixtures/guidance_compaction_baseline.json'
# Fixed before editing guidance: reduce the measured 9,001-character overhead by
# at least half. This is not a claim about total task tokens or behavioral quality.
MAX_LOADING_GUIDANCE_CHARACTERS = 4500


def loading_guidance_characters(root=ROOT):
    """Count every character in the two selectors and fifteen direct-entry guards.

    No strip(), token approximation, compression, or duplicated-text subtraction
    is used. The original 23 operational sections are checked separately.
    """
    root = Path(root)
    manifest = json.loads(BASELINE.read_text())
    advanced = root / 'skills/_coco-shared/advanced'
    measured = {}
    for family, original in manifest['families'].items():
        selection_characters = 0
        module_guard_characters = 0
        module_count = 0
        destinations = {row['destination'] for row in original['sections']}
        for name in sorted(destinations):
            preamble, blocks = split_sections((advanced / name).read_bytes().decode('utf-8'))
            if name == family + '.md':
                selection_characters += sum(
                    len(block) for heading, block in blocks if heading == 'Mode selection')
            else:
                module_guard_characters += len(preamble)
                module_count += 1
        measured[family] = {
            'selection_characters': selection_characters,
            'module_guard_characters': module_guard_characters,
            'module_count': module_count,
        }
    return {
        'families': measured,
        'total_characters': sum(
            family['selection_characters'] + family['module_guard_characters']
            for family in measured.values()),
    }


def inspect_guidance_budget(root=ROOT):
    """A missing selector, guard, or preserved section cannot earn cost savings."""
    failures = list(inspect_context_loading(root)['failures'])
    if failures:
        return {'failures': failures, 'measurement': None}
    measurement = loading_guidance_characters(root)
    total = measurement['total_characters']
    if total > MAX_LOADING_GUIDANCE_CHARACTERS:
        failures.append(('loading-guidance-budget',
                         f'{total} characters exceed {MAX_LOADING_GUIDANCE_CHARACTERS}'))
    return {'failures': failures, 'measurement': measurement}


class GuidanceCompactionTests(unittest.TestCase):
    def isolated_package(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        root = Path(scratch.name)
        shutil.copytree(ROOT / 'skills', root / 'skills')
        return root

    def test_loading_guidance_reduces_frozen_overhead_by_at_least_half(self):
        baseline = json.loads(COMPACTION_BASELINE.read_text())
        self.assertEqual(baseline['total_characters'], 9001)
        self.assertEqual(sum(
            family['selection_characters'] + family['module_guard_characters']
            for family in baseline['families'].values()), baseline['total_characters'])
        self.assertEqual(sum(family['module_count'] for family in
                             baseline['families'].values()), 15)
        self.assertLess(MAX_LOADING_GUIDANCE_CHARACTERS,
                        baseline['total_characters'] / 2)
        result = inspect_guidance_budget()
        self.assertEqual(result['failures'], [], result)

    def test_measurement_does_not_discount_whitespace_or_multibyte_text(self):
        root = self.isolated_package()
        before = loading_guidance_characters(root)['total_characters']
        path = root / 'skills/_coco-shared/advanced/verify-runtime-create.md'
        additional_guidance = '\r\n   \r\n한글\r\n'
        path.write_bytes(additional_guidance.encode('utf-8') + path.read_bytes())
        after = loading_guidance_characters(root)['total_characters']
        self.assertEqual(after - before, len(additional_guidance))

    def test_removing_a_direct_entry_guard_cannot_pass_the_budget_gate(self):
        root = self.isolated_package()
        path = root / 'skills/_coco-shared/advanced/automate-ci.md'
        _, blocks = split_sections(path.read_text())
        path.write_text(''.join(block for _, block in blocks))
        result = inspect_guidance_budget(root)
        self.assertIn('module-core-link', [code for code, _ in result['failures']])
        self.assertIsNone(result['measurement'])


if __name__ == '__main__':
    unittest.main()
