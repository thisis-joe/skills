"""Exercise durable TIL resolution with actual primary/linked Git repositories."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
RESOLVER = ROOT / 'skills/coco-til/tools/resolve_workspace.py'
spec = importlib.util.spec_from_file_location('til_workspace', RESOLVER)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class TilWorkspaceTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        self.primary = self.root / 'primary checkout'
        self.primary.mkdir()
        self.git(self.primary, 'init', '-b', 'trunk')
        self.git(self.primary, '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                 'commit', '--allow-empty', '-m', 'initial')
        self.linked = self.root / 'linked checkout'
        self.git(self.primary, 'worktree', 'add', '-b', 'feature', str(self.linked))

    def git(self, folder, *args):
        return subprocess.run(['git', '-C', str(folder), *args], check=True,
                              capture_output=True, text=True).stdout.strip()

    def resolve(self, folder):
        result = subprocess.run([sys.executable, str(RESOLVER), str(folder)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_ignored_notes_from_linked_tree_survive_its_removal(self):
        (self.primary / '.gitignore').write_text('TIL/\n')
        sub = self.linked / 'nested folder'
        sub.mkdir()
        result = self.resolve(sub)
        self.assertEqual(result, self.resolve(self.primary))
        self.assertEqual(result['til'], str(self.primary / 'TIL'))
        notes = Path(result['til'])
        notes.mkdir()
        (notes / 'concept.md').write_text('retain knowledge')
        self.assertEqual(self.git(self.primary, 'check-ignore', 'TIL/concept.md'),
                         'TIL/concept.md')
        self.git(self.primary, 'worktree', 'remove', '--force', str(self.linked))
        self.assertEqual((notes / 'concept.md').read_text(), 'retain knowledge')

    def test_non_git_resolution_is_read_only_and_missing_primary_fails_closed(self):
        outside = self.root / 'outside'
        outside.mkdir()
        result = self.resolve(outside)
        self.assertFalse(result['repository'])
        self.assertEqual(result['til'], str(outside / 'TIL'))
        self.assertEqual(list(outside.iterdir()), [])
        self.primary.rename(self.root / 'moved primary')
        with self.assertRaises(module.ResolutionError):
            module.resolve_workspace(self.linked)
        self.assertFalse((self.linked / 'TIL').exists())

    def test_bare_primary_and_symlinked_storage_are_not_fallbacks(self):
        bare = self.root / 'bare.git'
        self.git(self.root, 'init', '--bare', str(bare))
        bare_tree = self.root / 'bare linked'
        # Seed the bare repository, then create a valid linked checkout.
        self.git(bare, 'fetch', str(self.primary), 'trunk')
        self.git(bare, 'worktree', 'add', '--detach', str(bare_tree), 'FETCH_HEAD')
        for folder in (bare, bare_tree):
            with self.assertRaises(module.ResolutionError):
                module.resolve_workspace(folder)
            self.assertFalse((folder / 'TIL').exists())
        target = self.root / 'elsewhere'
        target.mkdir()
        (self.primary / 'TIL').symlink_to(target, target_is_directory=True)
        with self.assertRaises(module.ResolutionError):
            module.resolve_workspace(self.linked)
        self.assertEqual(list(target.iterdir()), [])

    def test_separate_git_dir_and_newline_path_use_git_identity(self):
        other = self.root / 'separate\ncheckout'
        metadata = self.root / 'metadata'
        self.git(self.root, 'init', '--separate-git-dir', str(metadata), str(other))
        self.assertEqual(self.resolve(other)['primary'], str(other))
        self.assertFalse((other / 'TIL').exists())


if __name__ == '__main__':
    unittest.main()
