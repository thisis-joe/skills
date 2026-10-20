"""Run the coco-merge preflight against real Git repositories with a bare remote."""
import json
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/coco-merge'
TOOL = SKILL / 'tools/merge_preflight.py'


class MergePreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.remote = base / 'remote.git'
        subprocess.run(['git', 'init', '-q', '--bare', '-b', 'main', str(self.remote)], check=True)
        self.work = self.clone('work')
        self.commit(self.work, 'app.txt', 'line one\n', 'baseline')
        self.git(self.work, 'push', '-q', 'origin', 'main')

    def clone(self, name):
        path = Path(self.temp.name) / name
        subprocess.run(['git', 'clone', '-q', str(self.remote), str(path)], check=True,
                       capture_output=True)
        self.git(path, 'config', 'user.email', 'fixture@example.test')
        self.git(path, 'config', 'user.name', 'Fixture')
        return path

    def git(self, repo, *args):
        return subprocess.check_output(['git', '-C', str(repo), *args], text=True).strip()

    def commit(self, repo, name, content, message):
        path = repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        self.git(repo, 'add', name)
        self.git(repo, 'commit', '-qm', message)
        return self.git(repo, 'rev-parse', 'HEAD')

    def feature(self, start='main', name='feat/x'):
        self.git(self.work, 'switch', '-qc', name, start)
        oid = self.commit(self.work, 'feature.txt', 'feature\n', 'feature work')
        self.git(self.work, 'push', '-q', '-u', 'origin', name)
        return oid

    def preflight(self, *args, expect=None, repo=None):
        result = subprocess.run([sys.executable, str(TOOL), '--repo', str(repo or self.work), *args],
                                capture_output=True, text=True)
        if expect is not None:
            self.assertEqual(result.returncode, expect, result.stdout + result.stderr)
        if result.returncode == 2:
            return result
        report = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1 if report['blockers'] else 0)
        return report

    def test_pushed_branch_is_clear_and_nothing_local_changes(self):
        head = self.feature()
        self.commit(self.clone('other'), 'app.txt', 'line one\nmain moved\n', 'main moves on')
        self.git(Path(self.temp.name) / 'other', 'push', '-q', 'origin', 'main')
        (self.work / 'notes.txt').write_text('user draft\n')
        refs = self.git(self.work, 'for-each-ref')
        status = self.git(self.work, 'status', '--porcelain=v1')
        report = self.preflight(expect=0)
        self.assertEqual((report['target'], report['head'], report['status']), ('main', head, 'clear'))
        self.assertEqual([row['subject'] for row in report['incoming']], ['feature work'])
        self.assertEqual(report['counts']['behind'], 1)
        self.assertEqual(report['warnings'], ['uncommitted_changes_excluded', 'behind_target'])
        self.assertIsNone(report['integration_base'])
        self.assertEqual(self.git(self.work, 'for-each-ref'), refs)
        self.assertEqual(self.git(self.work, 'status', '--porcelain=v1'), status)
        self.assertFalse((self.work / '.git/FETCH_HEAD').exists())

    def test_unpushed_local_commit_blocks(self):
        self.feature()
        self.commit(self.work, 'feature.txt', 'feature\nmore\n', 'not pushed yet')
        report = self.preflight(expect=1)
        self.assertEqual(report['blockers'], ['unpushed_commits'])
        self.assertEqual([row['subject'] for row in report['unpushed']], ['not pushed yet'])

    def test_commit_someone_else_pushed_to_the_branch_blocks(self):
        self.feature()
        other = self.clone('other')
        self.git(other, 'switch', '-q', 'feat/x')
        self.commit(other, 'other.txt', 'theirs\n', 'pushed by someone else')
        self.git(other, 'push', '-q', 'origin', 'feat/x')
        report = self.preflight(expect=1)
        self.assertEqual(report['blockers'], ['unknown_remote_commits'])
        self.assertEqual([row['subject'] for row in report['unknown_remote_commits']],
                         ['pushed by someone else'])

    def test_forge_update_merge_of_the_target_is_accepted(self):
        pushed = self.feature()
        other = self.clone('other')
        self.commit(other, 'app.txt', 'line one\nmain moved\n', 'main moves on')
        self.git(other, 'push', '-q', 'origin', 'main')
        self.git(other, 'switch', '-q', 'feat/x')
        self.git(other, 'merge', '-q', '--no-edit', 'origin/main')
        self.git(other, 'push', '-q', 'origin', 'feat/x')
        updated = self.git(other, 'rev-parse', 'HEAD')
        report = self.preflight('--expect-head', updated, expect=0)
        self.assertEqual(report['local_head'], pushed)
        self.assertEqual(report['head'], updated)
        self.assertEqual(report['counts']['update_merges'], 1)
        self.assertEqual(report['unknown_remote_commits'], [])

    def test_forge_head_that_differs_from_the_pushed_head_blocks(self):
        self.feature()
        report = self.preflight('--expect-head', self.git(self.work, 'rev-parse', 'main'), expect=1)
        self.assertEqual(report['blockers'], ['head_mismatch'])

    def test_develop_commits_carried_into_the_default_branch_block(self):
        self.git(self.work, 'switch', '-qc', 'develop')
        self.commit(self.work, 'unreleased.txt', 'later\n', 'unreleased develop work')
        self.git(self.work, 'push', '-q', 'origin', 'develop')
        self.feature(start='develop')
        report = self.preflight(expect=1)
        self.assertEqual(report['integration_base'], 'develop')
        self.assertEqual(report['blockers'], ['integration_commits_carried'])
        self.assertEqual([row['subject'] for row in report['carried']], ['unreleased develop work'])
        self.assertEqual([row['subject'] for row in report['own']], ['feature work'])
        into_develop = self.preflight('--target', 'develop', expect=0)
        self.assertIsNone(into_develop['integration_base'])
        self.assertEqual(into_develop['counts']['incoming'], 1)

    def test_branch_synced_with_develop_that_matches_main_is_clear(self):
        self.git(self.work, 'push', '-q', 'origin', 'main:refs/heads/develop')
        self.feature(start='main')
        report = self.preflight(expect=0)
        self.assertEqual(report['integration_base'], 'develop')
        self.assertEqual(report['counts']['carried'], 0)

    def test_both_dev_and_develop_need_an_explicit_integration_base(self):
        for name in ('dev', 'develop'):
            self.git(self.work, 'push', '-q', 'origin', 'main:refs/heads/' + name)
        self.feature()
        self.assertEqual(self.preflight(expect=1)['blockers'], ['integration_base_ambiguous'])
        chosen = self.preflight('--integration-base', 'develop', expect=0)
        self.assertEqual(chosen['integration_base'], 'develop')
        self.assertIsNone(self.preflight('--integration-base', 'none', expect=0)['integration_base'])

    def test_conflict_with_the_target_names_the_path(self):
        self.feature()
        self.commit(self.work, 'app.txt', 'feature edit\n', 'feature edits app')
        self.git(self.work, 'push', '-q', 'origin', 'feat/x')
        other = self.clone('other')
        self.commit(other, 'app.txt', 'main edit\n', 'main edits app')
        self.git(other, 'push', '-q', 'origin', 'main')
        report = self.preflight(expect=1)
        self.assertEqual(report['blockers'], ['conflicts'])
        self.assertEqual(report['conflicts'], {'status': 'conflict', 'paths': ['app.txt']})

    def test_branch_already_in_the_target_has_nothing_to_merge(self):
        self.feature()
        self.git(self.work, 'push', '-q', 'origin', 'feat/x:main')
        self.assertEqual(self.preflight(expect=1)['blockers'], ['nothing_to_merge'])

    def test_branch_missing_on_the_remote_blocks(self):
        self.git(self.work, 'switch', '-qc', 'feat/local-only')
        self.commit(self.work, 'local.txt', 'local\n', 'never pushed')
        self.assertEqual(self.preflight(expect=1)['blockers'], ['branch_not_on_remote'])

    def test_unusable_inputs_exit_two_rather_than_clear(self):
        self.feature()
        self.assertIn('not on origin', self.preflight('--target', 'release', expect=2).stderr)
        self.assertIn('invalid branch', self.preflight('--branch=-x', expect=2).stderr)
        self.git(self.work, 'switch', '-q', '--detach')
        self.assertIn('pass --branch', self.preflight(expect=2).stderr)
        self.assertEqual(self.preflight('--branch', 'feat/x', expect=0)['status'], 'clear')

    def test_skill_documents_every_code_and_the_exit_contract(self):
        codes = runpy.run_path(str(TOOL))
        skill = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        reference = (SKILL / 'references/forge-merge.md').read_text(encoding='utf-8')
        self.assertIn('(tools/merge_preflight.py)', skill)
        self.assertIn('never read 2 as clear', skill)
        for code in codes['BLOCKERS'] + codes['WARNINGS']:
            self.assertIn('`%s`' % code, reference, code)
        for forbidden in ('--admin', '--rebase'):
            self.assertIn('`%s`' % forbidden, reference)


if __name__ == '__main__':
    unittest.main()
