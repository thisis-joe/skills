"""English source documents remain independent from localized user output."""
from pathlib import Path
import re
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
HANGUL = re.compile('[\u1100-\u11ff\u3130-\u318f\uac00-\ud7a3]')
LOCAL_FRAGMENT = re.compile(r'\]\(([^):\s]+\.md)#([^\s)]+)\)')


def hangul_locations(skills):
    failures = []
    for path in sorted(Path(skills).rglob('*')):
        if path.is_file() and path.suffix in ('.md', '.yaml', '.yml'):
            failures.extend(
                f'{path.relative_to(skills)}:{number}'
                for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1)
                if HANGUL.search(line))
    return failures


def fragment_failures(skills):
    failures = []
    for path in Path(skills).rglob('*.md'):
        for target, fragment in LOCAL_FRAGMENT.findall(path.read_text(encoding='utf-8')):
            destination = (path.parent / target).resolve()
            if not destination.is_file():
                failures.append(f'{path}: missing {target}')
                continue
            headings = re.findall(r'^#{1,6}\s+(.+)$', destination.read_text(encoding='utf-8'), re.M)
            slugs = {re.sub(r'[^\w\s-]', '', heading).lower().replace(' ', '-')
                     for heading in headings}
            if fragment not in slugs:
                failures.append(f'{path}: missing {target}#{fragment}')
    return failures


class SkillLanguageTests(unittest.TestCase):
    def test_active_instruction_documents_have_no_hangul(self):
        # License attribution is legal evidence, not an instruction document.
        # Human bilingual review also checks that English preserves the behavior.
        self.assertEqual(hangul_locations(ROOT / 'skills'), [])

    def test_detection_includes_discovery_metadata_and_references(self):
        with tempfile.TemporaryDirectory() as directory:
            skills = Path(directory)
            (skills / 'SKILL.md').write_text('description: "English \ud55c\uae00"\n', encoding='utf-8')
            (skills / 'reference.md').write_text('# English\n\u1100\n', encoding='utf-8')
            (skills / 'LICENSE').write_text('\ud55c\uae00 legal attribution\n', encoding='utf-8')
            self.assertEqual(hangul_locations(skills), ['SKILL.md:1', 'reference.md:2'])

    def test_local_document_heading_links_resolve(self):
        self.assertEqual(fragment_failures(ROOT / 'skills'), [])


if __name__ == '__main__':
    unittest.main()
