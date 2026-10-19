"""Check lossless conditional-document extraction, not agent performance equivalence."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / 'tests/fixtures/context_loading_baseline.json'
SECTION = re.compile(r'^## ([^\r\n]+)\n', re.MULTILINE)
LINK = re.compile(r'\[[^\]\n]+\]\(([^)\n]+)\)')


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def split_sections(text):
    """Retain headings, blank lines and final newlines in each original block."""
    matches = list(SECTION.finditer(text))
    preamble = text[:matches[0].start()] if matches else text
    blocks = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks.append((match.group(1), text[match.start():end]))
    return preamble, blocks


def local_links(text, source):
    """Resolve Markdown file links from the file that actually owns the text."""
    for match in LINK.finditer(text):
        target = match.group(1).strip()
        if target.startswith('<') and target.endswith('>'):
            target = target[1:-1]
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        yield match, (source.parent / unquote(parsed.path)).resolve()


def inspect_context_loading(root=ROOT, baseline=None):
    """Return structured failures; callers can inject an isolated package root."""
    root = Path(root)
    if baseline is None:
        baseline = json.loads(BASELINE.read_text())
    advanced = root / 'skills/_coco-shared/advanced'
    documents = {
        path.name: (path, *split_sections(path.read_bytes().decode('utf-8')))
        for path in advanced.glob('*.md')
    }
    failures = []
    reconstructions = {}

    def fail(code, detail):
        failures.append((code, detail))

    for family, original in baseline['families'].items():
        router_name = family + '.md'
        rows = original['sections']
        expected_files = {row['destination'] for row in rows}
        actual_files = {
            name for name in documents
            if name == router_name or name.startswith(family + '-')
        }
        for name in sorted(expected_files - actual_files):
            fail('missing-file', name)
        for name in sorted(actual_files - expected_files):
            fail('unexpected-file', name)

        expected_headings = {row['heading'] for row in rows}
        owners = {heading: [] for heading in expected_headings}
        for name, (path, preamble, blocks) in documents.items():
            managed = name in actual_files
            if managed:
                if name == router_name:
                    if preamble != original['preamble']:
                        fail('preamble', name)
                else:
                    # A directly opened module must lead back to its family core.
                    # The preserved original starts at its first level-two heading.
                    guard_targets = {target for _, target in local_links(preamble, path)}
                    if not preamble.strip() or (advanced / router_name).resolve() not in guard_targets:
                        fail('module-core-link', name)
                mode_count = sum(heading == 'Mode selection' for heading, _ in blocks)
                if mode_count != (1 if name == router_name else 0):
                    fail('mode-selection', name)
                headings = [heading for heading, _ in blocks if heading != 'Mode selection']
                expected_order = [row['heading'] for row in rows if row['destination'] == name]
                if headings != expected_order:
                    fail('section-order', name)
                for heading, block in blocks:
                    if heading not in expected_headings and not (
                            name == router_name and heading == 'Mode selection'):
                        fail('unexpected-section', name + ': ' + heading)
                for _, target in local_links(path.read_bytes().decode('utf-8'), path):
                    if not target.is_file():
                        fail('broken-relative-link', name + ': ' + str(target))

            for index, (heading, block) in enumerate(blocks):
                if heading not in owners:
                    continue
                row = next(row for row in rows if row['heading'] == heading)
                # Generic headings in unrelated procedures are not duplicate ownership.
                # An exact original block copied there is a duplicate nonetheless.
                if managed or digest(block) == row['sha256']:
                    owners[heading].append((name, index, block))

        restored = []
        for row in rows:
            matches = owners[row['heading']]
            if not matches:
                fail('missing-section', row['heading'])
                continue
            if len(matches) != 1:
                fail('duplicate-section', row['heading'])
                continue
            name, _, block = matches[0]
            if name != row['destination']:
                fail('wrong-owner', row['heading'] + ': ' + name)
            if digest(block) != row['sha256'] or len(block) != row['characters']:
                fail('section-content', row['heading'])
            restored.append(block)

        # The original interleaving comes from the frozen manifest, not file order.
        reconstructed = original['preamble'] + ''.join(restored)
        reconstructions[family] = digest(reconstructed)
        if (digest(reconstructed) != original['original_sha256'] or
                len(reconstructed) != original['original_characters']):
            fail('reconstructed-original', family)

        if router_name in documents:
            router_path, _, router_blocks = documents[router_name]
            selection = [block for heading, block in router_blocks if heading == 'Mode selection']
            direct_targets = {
                target for block in selection for _, target in local_links(block, router_path)
            }
            for name in sorted(expected_files - {router_name}):
                if (advanced / name).resolve() not in direct_targets:
                    fail('unreachable-module', name)

    return {'failures': failures, 'reconstructed_sha256': reconstructions}


class ContextLoadingTests(unittest.TestCase):
    def assert_valid(self, root=ROOT):
        result = inspect_context_loading(root)
        self.assertEqual(result['failures'], [], '\n'.join(
            code + ': ' + detail for code, detail in result['failures']))
        return result

    def isolated_package(self):
        self.assert_valid()
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        root = Path(scratch.name)
        shutil.copytree(ROOT / 'skills', root / 'skills')
        self.assert_valid(root)
        return root

    def advanced(self, root):
        return root / 'skills/_coco-shared/advanced'

    def assert_detected(self, root, code):
        failures = inspect_context_loading(root)['failures']
        self.assertIn(code, [kind for kind, _ in failures], failures)

    def test_original_sections_are_preserved_once_and_reassemble_exactly(self):
        result = self.assert_valid()
        baseline = json.loads(BASELINE.read_text())
        self.assertEqual(result['reconstructed_sha256'], {
            family: original['original_sha256']
            for family, original in baseline['families'].items()
        })

    def test_missing_module_is_detected(self):
        root = self.isolated_package()
        (self.advanced(root) / 'verify-runtime-create.md').unlink()
        self.assert_detected(root, 'missing-file')
        self.assert_detected(root, 'missing-section')

    def test_changed_original_instruction_is_detected(self):
        root = self.isolated_package()
        path = self.advanced(root) / 'automate-ci.md'
        path.write_bytes(path.read_bytes() + b'Changed instruction.\n')
        self.assert_detected(root, 'section-content')
        self.assert_detected(root, 'reconstructed-original')

    def test_duplicate_section_in_router_is_detected(self):
        root = self.isolated_package()
        advanced = self.advanced(root)
        router = advanced / 'verify.md'
        router.write_bytes(router.read_bytes() + (advanced / 'verify-formal-create.md').read_bytes())
        self.assert_detected(root, 'duplicate-section')

    def test_duplicate_original_in_an_unrelated_document_is_detected(self):
        root = self.isolated_package()
        advanced = self.advanced(root)
        with (advanced / 'debug.md').open('ab') as output:
            output.write((advanced / 'verify-formal-create.md').read_bytes())
        self.assert_detected(root, 'duplicate-section')

    def test_router_must_link_to_every_module_in_its_selection_section(self):
        root = self.isolated_package()
        advanced = self.advanced(root)
        router = advanced / 'verify.md'
        text = router.read_bytes().decode('utf-8')
        target = (advanced / 'verify-formal-maintain.md').resolve()
        links = [match for match, resolved in local_links(text, router) if resolved == target]
        self.assertTrue(links, 'Fixture must include the link this mutation removes')
        for match in reversed(links):
            text = text[:match.start()] + 'Unlinked mode' + text[match.end():]
        router.write_bytes(text.encode('utf-8'))
        self.assert_detected(root, 'unreachable-module')

    def test_module_relative_links_are_checked_from_their_new_owner(self):
        root = self.isolated_package()
        path = self.advanced(root) / 'verify-quality-audit.md'
        preamble, blocks = split_sections(path.read_bytes().decode('utf-8'))
        body = ''.join(block for _, block in blocks)
        links = list(local_links(body, path))
        self.assertTrue(links, 'Fixture must contain a relative reference')
        match, _ = links[0]
        path.write_bytes((preamble + body[:match.start()] + '[broken](missing-procedure.md)' +
                          body[match.end():]).encode('utf-8'))
        self.assert_detected(root, 'broken-relative-link')

    def test_directly_opened_module_must_lead_back_to_its_core(self):
        root = self.isolated_package()
        path = self.advanced(root) / 'automate-ci.md'
        _, blocks = split_sections(path.read_bytes().decode('utf-8'))
        path.write_bytes(''.join(block for _, block in blocks).encode('utf-8'))
        self.assert_detected(root, 'module-core-link')

    def test_router_preamble_cannot_change_during_extraction(self):
        root = self.isolated_package()
        path = self.advanced(root) / 'automate.md'
        path.write_bytes(b'Additional instruction.\n' + path.read_bytes())
        self.assert_detected(root, 'preamble')

    def test_original_core_section_cannot_move_to_a_different_owner(self):
        root = self.isolated_package()
        advanced = self.advanced(root)
        router = advanced / 'verify.md'
        preamble, blocks = split_sections(router.read_bytes().decode('utf-8'))
        heading, block = next(item for item in blocks if item[0] == 'Behavioral checks')
        router.write_bytes((preamble + ''.join(value for name, value in blocks
                                              if name != heading)).encode('utf-8'))
        with (advanced / 'verify-runtime-create.md').open('ab') as output:
            output.write(block.encode('utf-8'))
        self.assert_detected(root, 'wrong-owner')

    def test_only_the_router_may_add_a_mode_selection_section(self):
        root = self.isolated_package()
        path = self.advanced(root) / 'automate-webhook.md'
        path.write_bytes(path.read_bytes() + b'## Mode selection\n\nExtra procedure.\n')
        self.assert_detected(root, 'mode-selection')

    def test_original_core_order_is_preserved(self):
        root = self.isolated_package()
        path = self.advanced(root) / 'automate.md'
        preamble, blocks = split_sections(path.read_bytes().decode('utf-8'))
        core_positions = [index for index, (name, _) in enumerate(blocks)
                          if name != 'Mode selection']
        first, second = core_positions[:2]
        blocks[first], blocks[second] = blocks[second], blocks[first]
        path.write_bytes((preamble + ''.join(block for _, block in blocks)).encode('utf-8'))
        self.assert_detected(root, 'section-order')


if __name__ == '__main__':
    unittest.main()
