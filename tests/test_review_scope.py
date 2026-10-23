import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'review_scope.py'
CANONICAL = SCRIPT.parent.parent / 'skills/_coco-shared/tools/review_scope.py'


class ReviewScopeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.git('init', '-q')
        self.git('config', 'user.email', 'fixture@example.test')
        self.git('config', 'user.name', 'Fixture')
        self.write('tracked.txt', 'original\n')
        self.write('deleted.txt', 'keep until next change\n')
        self.git('add', '.')
        self.git('commit', '-qm', 'baseline')
        self.base = self.git('rev-parse', 'HEAD').strip()

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.repo), *args], text=True)

    def write(self, name, content):
        p = self.repo / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding='utf-8')

    def run_scope(self, *args, expect=0):
        result = subprocess.run([sys.executable, str(SCRIPT), '--repo', str(self.repo),
                                 '--base', self.base, *args], capture_output=True, text=True)
        self.assertEqual(result.returncode, expect, result.stderr)
        return json.loads(result.stdout) if expect == 0 else result

    def test_reports_all_four_layers_including_untracked(self):
        self.write('committed.txt', 'committed\n')
        self.git('add', 'committed.txt')
        self.git('commit', '-qm', 'feature slice')
        self.write('tracked.txt', 'staged\n')
        self.git('add', 'tracked.txt')
        self.write('tracked.txt', 'working\n')
        self.write('new file.txt', 'new\n')
        files = {f['path']: f for f in self.run_scope()['files']}
        self.assertEqual(files['committed.txt']['layers'], ['committed'])
        self.assertEqual(files['tracked.txt']['layers'], ['staged', 'worktree'])
        self.assertEqual(files['new file.txt']['layers'], ['untracked'])

    def test_deleted_and_unusual_filenames_are_not_lost(self):
        (self.repo / 'deleted.txt').unlink()
        # Windows forbids control characters in names; keep the newline case elsewhere.
        unusual = 'line\nbreak.txt' if os.name != 'nt' else 'space and \u00fc.txt'
        self.write(unusual, 'new\n')
        files = {f['path']: f for f in self.run_scope()['files']}
        self.assertEqual(files['deleted.txt']['statuses']['worktree'], 'D')
        self.assertIn(unusual, files)

    def test_task_paths_are_literal_and_directory_scopes_work(self):
        self.write('[x].txt', 'literal\n')
        self.write('x.txt', 'not selected\n')
        self.write('feature/one.txt', 'selected\n')
        scoped = self.run_scope('--path', '[x].txt', '--path', 'feature')
        self.assertEqual({f['path'] for f in scoped['files']}, {'[x].txt', 'feature/one.txt'})

    def test_collecting_scope_does_not_modify_git_or_files(self):
        self.write('tracked.txt', 'changed\n')
        self.write('new.txt', 'not staged\n')
        before = self.git('status', '--porcelain=v1', '-z')
        head = self.git('rev-parse', 'HEAD')
        self.run_scope()
        self.assertEqual(self.git('status', '--porcelain=v1', '-z'), before)
        self.assertEqual(self.git('rev-parse', 'HEAD'), head)
        self.assertEqual((self.repo / 'new.txt').read_text(encoding='utf-8'), 'not staged\n')

    def test_fingerprint_changes_when_reviewed_content_changes(self):
        self.write('tracked.txt', 'first\n')
        first = self.run_scope()['snapshot']
        self.write('tracked.txt', 'second\n')
        self.assertNotEqual(first, self.run_scope()['snapshot'])

    def test_fingerprint_includes_staged_content_not_just_worktree(self):
        self.write('tracked.txt', 'stage one\n')
        self.git('add', 'tracked.txt')
        self.write('tracked.txt', 'same worktree\n')
        first = self.run_scope()['snapshot']
        self.write('tracked.txt', 'stage two\n')
        self.git('add', 'tracked.txt')
        self.write('tracked.txt', 'same worktree\n')
        self.assertNotEqual(first, self.run_scope()['snapshot'])

    def test_invalid_base_and_escaping_scope_fail_clearly(self):
        self.base = 'missing-ref'
        self.assertIn('base', self.run_scope(expect=2).stderr.lower())
        self.base = self.git('rev-parse', 'HEAD').strip()
        self.assertIn('path', self.run_scope('--path', '../outside', expect=2).stderr.lower())

    def test_clean_repository_returns_empty_scope(self):
        result = self.run_scope()
        self.assertFalse(result['has_changes'])
        self.assertEqual(result['files'], [])

    def test_nested_repository_argument_uses_root_paths_and_real_content(self):
        self.write('feature/tracked.txt', 'baseline\n')
        self.git('add', 'feature/tracked.txt')
        self.git('commit', '-qm', 'nested baseline')
        self.base = self.git('rev-parse', 'HEAD').strip()
        self.write('feature/tracked.txt', 'staged\n')
        self.git('add', 'feature/tracked.txt')
        self.write('feature/tracked.txt', 'one\n')
        self.write('feature/new.txt', 'untracked\n')

        def nested_scope():
            result = subprocess.run([sys.executable, str(SCRIPT), '--repo', str(self.repo / 'feature'),
                                     '--base', self.base], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(result.stdout)

        first = nested_scope()
        self.assertEqual(first['repository'], str(self.repo.resolve()))
        self.assertEqual({f['path'] for f in first['files']}, {'feature/tracked.txt', 'feature/new.txt'})
        tracked = next(f for f in first['files'] if f['path'] == 'feature/tracked.txt')
        self.assertEqual(tracked['layers'], ['staged', 'worktree'])
        self.write('feature/tracked.txt', 'two\n')
        self.assertNotEqual(first['snapshot'], nested_scope()['snapshot'])

    def test_nested_collect_api_honors_root_relative_literal_filter(self):
        self.write('feature/tracked.txt', 'baseline\n')
        self.git('add', 'feature/tracked.txt')
        self.git('commit', '-qm', 'nested baseline')
        base = self.git('rev-parse', 'HEAD').strip()
        self.write('feature/tracked.txt', 'changed\n')
        self.write('feature/new.txt', 'new\n')
        collect = runpy.run_path(str(CANONICAL))['collect']
        result = collect(self.repo / 'feature', base, ['feature'])
        self.assertEqual(result['repository'], str(self.repo.resolve()))
        self.assertEqual({f['path'] for f in result['files']}, {'feature/tracked.txt', 'feature/new.txt'})
        selected = collect(self.repo / 'feature', base, ['feature/new.txt'])
        self.assertEqual([f['path'] for f in selected['files']], ['feature/new.txt'])


if __name__ == '__main__':
    unittest.main()
