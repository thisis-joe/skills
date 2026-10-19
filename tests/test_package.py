import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'package'
        self.dest = Path(self.temp.name) / 'installed'
        self.root.mkdir()
        self.write('lets.json', json.dumps({'schema': 1, 'display_prefix': "let's-",
            'invocation_prefix': 'lets-', 'shared': '_lets-shared', 'skills': ['lets-example']}))
        self.write('skills/_lets-shared/contracts.md', '# Common contract\n')
        self.write('skills/lets-example/SKILL.md', '---\nname: lets-example\n'
                   'description: "Use when testing the installed package."\nlicense: MIT\n---\n'
                   '# Example\n\nRead [contract](../_lets-shared/contracts.md).\n')
        self.write('skills/lets-example/agents/openai.yaml', 'interface:\n'
                   '  display_name: "let\'s-example"\n'
                   '  short_description: "A concrete fixture for package installation"\n'
                   '  default_prompt: "Use $lets-example for this task."\n')

    def write(self, rel, value):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(value)

    def run_tool(self, name, *args, expect=0):
        command = [sys.executable, str(ROOT / 'scripts' / name), '--root', str(self.root), *args]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, expect, result.stdout + result.stderr)
        return result

    def install(self, *args, expect=0):
        return self.run_tool('install.py', '--dest', str(self.dest), *args, expect=expect)

    def test_installs_shared_contract_and_references_remain_valid(self):
        self.install()
        self.assertTrue((self.dest / '_lets-shared/contracts.md').is_file())
        self.assertEqual((self.dest / 'lets-example/SKILL.md').read_bytes(),
                         (self.root / 'skills/lets-example/SKILL.md').read_bytes())
        self.run_tool('validate.py', '--installed', str(self.dest))

    def test_dry_run_does_not_create_destination(self):
        self.install('--dry-run')
        self.assertFalse(self.dest.exists())

    def test_installation_is_idempotent(self):
        self.install()
        manifest = (self.dest / '.lets-install.json').read_bytes()
        file = self.dest / 'lets-example/SKILL.md'
        modified_time = file.stat().st_mtime_ns
        self.install()
        self.assertEqual(manifest, (self.dest / '.lets-install.json').read_bytes())
        self.assertEqual(modified_time, file.stat().st_mtime_ns)

    def test_foreign_skill_conflict_prevents_all_writes(self):
        folder = self.dest / 'lets-example'
        folder.mkdir(parents=True)
        (folder / 'SKILL.md').write_text('user-owned')
        self.install(expect=2)
        self.assertEqual((folder / 'SKILL.md').read_text(), 'user-owned')
        self.assertFalse((self.dest / '_lets-shared').exists())

    def test_modified_managed_file_is_preserved_on_update(self):
        self.install()
        target = self.dest / 'lets-example/SKILL.md'
        target.write_text('user modification')
        self.write('skills/_lets-shared/contracts.md', 'new version\n')
        self.install(expect=2)
        self.assertEqual(target.read_text(), 'user modification')
        self.assertEqual((self.dest / '_lets-shared/contracts.md').read_text(), '# Common contract\n')

    def test_unmodified_managed_install_can_update(self):
        self.install()
        self.write('skills/_lets-shared/contracts.md', '# Updated contract\n')
        self.install()
        self.assertEqual((self.dest / '_lets-shared/contracts.md').read_text(), '# Updated contract\n')

    def test_extra_user_file_in_managed_directory_prevents_update(self):
        self.install()
        extra = self.dest / 'lets-example/notes.txt'
        extra.write_text('do not delete')
        self.write('skills/_lets-shared/contracts.md', 'new version\n')
        self.install(expect=2)
        self.assertEqual(extra.read_text(), 'do not delete')

    def test_other_installed_skills_are_untouched(self):
        other = self.dest / 'unrelated/SKILL.md'
        other.parent.mkdir(parents=True)
        other.write_text('unrelated')
        self.install()
        self.assertEqual(other.read_text(), 'unrelated')

    def test_symlink_in_package_or_target_is_refused(self):
        secret = Path(self.temp.name) / 'outside.txt'
        secret.write_text('external')
        (self.root / 'skills/lets-example/link').symlink_to(secret)
        self.install(expect=2)
        self.assertFalse(self.dest.exists())
        (self.root / 'skills/lets-example/link').unlink()
        self.dest.symlink_to(self.root / 'skills', target_is_directory=True)
        self.install(expect=2)

    def test_manifest_cannot_escape_destination(self):
        config = json.loads((self.root / 'lets.json').read_text())
        config['skills'] = ['../outside']
        self.write('lets.json', json.dumps(config))
        self.install(expect=2)
        self.assertFalse(self.dest.exists())

    def test_broken_reference_and_wrong_name_are_rejected(self):
        self.write('skills/_lets-shared/contracts.md', '[bad](missing.md)\n')
        self.run_tool('validate.py', expect=2)
        self.write('skills/_lets-shared/contracts.md', '# Restored\n')
        p = self.root / 'skills/lets-example/SKILL.md'
        p.write_text(p.read_text().replace('name: lets-example', 'name: wrong-name'))
        self.run_tool('validate.py', expect=2)

    def test_installed_tampering_is_detected(self):
        self.install()
        (self.dest / '_lets-shared/contracts.md').write_text('tampered')
        self.run_tool('validate.py', '--installed', str(self.dest), expect=2)

    def test_source_checksum_and_coverage_are_verified(self):
        raw = b'original upstream skill\n'
        self.write('sources/a/SKILL.md.source', raw.decode())
        source = {'author': 'a', 'path': 'skills/example/SKILL.md',
                  'local': 'sources/a/SKILL.md.source', 'sha256': hashlib.sha256(raw).hexdigest()}
        self.write('sources/manifest.json', json.dumps({'files': [source]}))
        row = {'author': 'a', 'path': source['path'], 'family': 'example',
               'disposition': 'adapted', 'essential_rules': ['Retain the actual behavior.'],
               'adaptation': 'Adapt the execution environment.',
               'implemented_references': ['skills/lets-example/SKILL.md']}
        self.write('sources/coverage.json', json.dumps({'entries': [row]}))
        self.run_tool('validate.py')
        self.write('sources/a/SKILL.md.source', 'modified original')
        self.run_tool('validate.py', expect=2)
        self.write('sources/a/SKILL.md.source', raw.decode())
        self.write('sources/coverage.json', json.dumps({'entries': []}))
        self.run_tool('validate.py', expect=2)


if __name__ == '__main__':
    unittest.main()
