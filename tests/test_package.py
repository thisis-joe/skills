from contextlib import redirect_stderr, redirect_stdout
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import install as installer
from install import default_destination


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'package'
        self.dest = Path(self.temp.name) / 'installed'
        self.root.mkdir()
        self.write('coco.json', json.dumps({'schema': 1, 'display_prefix': "coco-",
            'invocation_prefix': 'coco-', 'shared': '_coco-shared', 'skills': ['coco-example']}))
        self.write('skills/_coco-shared/contracts.md', '# Common contract\n')
        self.write('skills/coco-example/SKILL.md', '---\nname: coco-example\n'
                   'description: "Use when testing the installed package."\nlicense: MIT\n---\n'
                   '# Example\n\nRead [contract](../_coco-shared/contracts.md).\n')
        self.write('skills/coco-example/agents/openai.yaml', 'interface:\n'
                   '  display_name: "coco-example"\n'
                   '  short_description: "A concrete fixture for package installation"\n'
                   '  default_prompt: "Use $coco-example for this task."\n')

    def write(self, rel, value):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(value, encoding='utf-8')

    def run_tool(self, name, *args, expect=0, env=None):
        command = [sys.executable, str(ROOT / 'scripts' / name), '--root', str(self.root), *args]
        # Without a terminal on stdin the installer never prompts, even when tests run in one.
        result = subprocess.run(command, capture_output=True, text=True, env=env,
                                stdin=subprocess.DEVNULL)
        self.assertEqual(result.returncode, expect, result.stdout + result.stderr)
        return result

    def install(self, *args, expect=0):
        return self.run_tool('install.py', '--dest', str(self.dest), *args, expect=expect)

    def test_installs_shared_contract_and_references_remain_valid(self):
        self.install()
        self.assertTrue((self.dest / '_coco-shared/contracts.md').is_file())
        self.assertEqual((self.dest / 'coco-example/SKILL.md').read_bytes(),
                         (self.root / 'skills/coco-example/SKILL.md').read_bytes())
        self.run_tool('validate.py', '--installed', str(self.dest))

    def test_dry_run_does_not_create_destination(self):
        self.install('--dry-run')
        self.assertFalse(self.dest.exists())

    def claude_env(self):
        return {**os.environ, 'CLAUDE_CONFIG_DIR': str(Path(self.temp.name) / 'claude')}

    def test_runtime_defaults_keep_codex_and_claude_separate(self):
        task_home = Path(self.temp.name) / 'home'
        with patch('install.Path.home', return_value=task_home), patch.dict(
                os.environ, {'CLAUDE_CONFIG_DIR': '', 'CODEX_HOME': ''}):
            self.assertEqual(default_destination('codex'), task_home / '.codex/skills')
            self.assertEqual(default_destination('claude'), task_home / '.claude/skills')
        with patch('install.Path.home', return_value=task_home), patch.dict(
                os.environ, {**self.claude_env(), 'CODEX_HOME': ''}):
            self.assertEqual(default_destination('codex'), task_home / '.codex/skills')

    def test_each_runtime_uses_only_its_own_config_home(self):
        codex_config = Path(self.temp.name) / 'codex config'
        claude_config = Path(self.temp.name) / 'claude config'
        with patch.dict(os.environ, {'CODEX_HOME': str(codex_config),
                                    'CLAUDE_CONFIG_DIR': str(claude_config)}):
            self.assertEqual(default_destination('codex'), codex_config / 'skills')
            self.assertEqual(default_destination('claude'), claude_config / 'skills')

    def test_claude_runtime_installs_into_its_configured_skills_directory(self):
        env = self.claude_env()
        dest = Path(env['CLAUDE_CONFIG_DIR']) / 'skills'
        result = self.run_tool('install.py', '--runtime', 'claude', env=env)
        self.assertEqual(json.loads(result.stdout)['destination'], str(dest))
        self.assertEqual((dest / 'coco-example/SKILL.md').read_bytes(),
                         (self.root / 'skills/coco-example/SKILL.md').read_bytes())
        self.assertTrue((dest / '_coco-shared/contracts.md').is_file())
        self.run_tool('validate.py', '--installed', str(dest))
        second = self.run_tool('install.py', '--runtime', 'claude', env=env)
        self.assertEqual(json.loads(second.stdout)['status'], 'unchanged')

    def test_claude_dry_run_does_not_create_config_directory(self):
        env = self.claude_env()
        result = self.run_tool('install.py', '--runtime', 'claude', '--dry-run', env=env)
        self.assertEqual(json.loads(result.stdout)['status'], 'dry-run')
        self.assertFalse(Path(env['CLAUDE_CONFIG_DIR']).exists())

    def test_claude_explicit_project_destination_overrides_user_config(self):
        env = self.claude_env()
        dest = Path(self.temp.name) / 'project/.claude/skills'
        self.run_tool('install.py', '--runtime', 'claude', '--dest', str(dest), env=env)
        self.assertTrue((dest / 'coco-example/SKILL.md').is_file())
        self.assertFalse(Path(env['CLAUDE_CONFIG_DIR']).exists())
        self.run_tool('validate.py', '--installed', str(dest))

    def test_codex_and_claude_destinations_can_be_installed_independently(self):
        self.install('--runtime', 'codex')
        before = (self.dest / '.coco-install.json').read_bytes()
        env = self.claude_env()
        self.run_tool('install.py', '--runtime', 'claude', env=env)
        self.assertEqual((self.dest / '.coco-install.json').read_bytes(), before)
        self.run_tool('validate.py', '--installed', str(self.dest))

    def test_claude_runtime_preserves_foreign_and_modified_skills(self):
        env = self.claude_env()
        dest = Path(env['CLAUDE_CONFIG_DIR']) / 'skills'
        other = dest / 'unrelated/SKILL.md'
        other.parent.mkdir(parents=True)
        other.write_text('user-owned unrelated skill', encoding='utf-8')
        self.run_tool('install.py', '--runtime', 'claude', env=env)
        managed = dest / 'coco-example/SKILL.md'
        managed.write_text('personal change', encoding='utf-8')
        self.write('skills/_coco-shared/contracts.md', 'new version\n')
        self.run_tool('install.py', '--runtime', 'claude', env=env, expect=2)
        self.assertEqual(managed.read_text(encoding='utf-8'), 'personal change')
        self.assertEqual(other.read_text(encoding='utf-8'), 'user-owned unrelated skill')
        self.assertEqual((dest / '_coco-shared/contracts.md').read_text(encoding='utf-8'), '# Common contract\n')

    def test_unknown_runtime_is_rejected_before_writing(self):
        self.install('--runtime', 'unsupported', expect=2)
        self.assertFalse(self.dest.exists())

    def test_installation_is_idempotent(self):
        self.install()
        manifest = (self.dest / '.coco-install.json').read_bytes()
        file = self.dest / 'coco-example/SKILL.md'
        modified_time = file.stat().st_mtime_ns
        self.install()
        self.assertEqual(manifest, (self.dest / '.coco-install.json').read_bytes())
        self.assertEqual(modified_time, file.stat().st_mtime_ns)

    def test_foreign_skill_conflict_prevents_all_writes(self):
        folder = self.dest / 'coco-example'
        folder.mkdir(parents=True)
        (folder / 'SKILL.md').write_text('user-owned', encoding='utf-8')
        self.install(expect=2)
        self.assertEqual((folder / 'SKILL.md').read_text(encoding='utf-8'), 'user-owned')
        self.assertFalse((self.dest / '_coco-shared').exists())

    def test_modified_managed_file_is_preserved_on_update(self):
        self.install()
        target = self.dest / 'coco-example/SKILL.md'
        target.write_text('user modification', encoding='utf-8')
        self.write('skills/_coco-shared/contracts.md', 'new version\n')
        self.install(expect=2)
        self.assertEqual(target.read_text(encoding='utf-8'), 'user modification')
        self.assertEqual((self.dest / '_coco-shared/contracts.md').read_text(encoding='utf-8'), '# Common contract\n')

    def test_unmodified_managed_install_can_update(self):
        self.install()
        self.write('skills/_coco-shared/contracts.md', '# Updated contract\n')
        self.install()
        self.assertEqual((self.dest / '_coco-shared/contracts.md').read_text(encoding='utf-8'), '# Updated contract\n')

    def test_extra_user_file_in_managed_directory_prevents_update(self):
        self.install()
        extra = self.dest / 'coco-example/notes.txt'
        extra.write_text('do not delete', encoding='utf-8')
        self.write('skills/_coco-shared/contracts.md', 'new version\n')
        self.install(expect=2)
        self.assertEqual(extra.read_text(encoding='utf-8'), 'do not delete')

    def test_other_installed_skills_are_untouched(self):
        other = self.dest / 'unrelated/SKILL.md'
        other.parent.mkdir(parents=True)
        other.write_text('unrelated', encoding='utf-8')
        self.install()
        self.assertEqual(other.read_text(encoding='utf-8'), 'unrelated')

    def git(self, repo, *args, expect=0):
        result = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True)
        self.assertEqual(result.returncode, expect, result.stdout + result.stderr)
        return result.stdout

    def test_dedicated_worktree_installs_branch_version_and_preserves_starting_checkout(self):
        self.git(self.root, 'init', '-q', '-b', 'main')
        self.git(self.root, 'config', 'user.email', 'fixture@example.test')
        self.git(self.root, 'config', 'user.name', 'Fixture')
        self.git(self.root, 'add', '.')
        self.git(self.root, 'commit', '-qm', 'baseline')
        self.git(self.root, 'switch', '-qc', 'feat/unrelated-work')
        skill = 'skills/coco-example/SKILL.md'
        user_edit = (self.root / skill).read_text(encoding='utf-8') + 'Personal uncommitted edit.\n'
        self.write(skill, user_edit)
        self.write('notes.txt', 'untracked user note\n')
        starting = [self.git(self.root, *args) for args in
                    (['branch', '--show-current'], ['rev-parse', 'HEAD'], ['status', '--porcelain'])]

        worktree = Path(self.temp.name) / 'skill-update'
        branch = 'feat/coco-example-team-rule'
        self.git(self.root, 'check-ref-format', '--branch', branch)
        self.git(self.root, 'worktree', 'add', '-q', '-b', branch, str(worktree), 'main')
        listed = self.git(self.root, 'worktree', 'list', '--porcelain')
        self.assertIn(f'worktree {worktree.resolve()}\n', listed)
        self.assertIn(f'branch refs/heads/{branch}\n', listed)
        self.assertNotIn('Personal uncommitted edit', (worktree / skill).read_text(encoding='utf-8'))
        self.assertFalse((worktree / 'notes.txt').exists())

        team_rule = (worktree / skill).read_text(encoding='utf-8') + 'Team rule from the dedicated branch.\n'
        (worktree / skill).write_text(team_rule, encoding='utf-8')
        self.git(worktree, 'commit', '-qam', 'feat: add team rule')
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/install.py'), '--root',
                                 str(worktree), '--dest', str(self.dest)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((self.dest / 'coco-example/SKILL.md').read_text(encoding='utf-8'), team_rule)

        # Git itself refuses a second checkout of the branch and an occupied path.
        self.git(self.root, 'worktree', 'add', '-q', str(Path(self.temp.name) / 'second'),
                 branch, expect=128)
        self.git(self.root, 'worktree', 'add', '-q', '-b', 'feat/other', str(self.dest),
                 'main', expect=128)
        self.assertEqual([self.git(self.root, *args) for args in
                          (['branch', '--show-current'], ['rev-parse', 'HEAD'],
                           ['status', '--porcelain'])], starting)
        self.assertEqual((self.root / skill).read_text(encoding='utf-8'), user_edit)
        self.assertEqual((self.root / 'notes.txt').read_text(encoding='utf-8'), 'untracked user note\n')

    def project(self, rel='project', git=True):
        folder = Path(self.temp.name) / rel
        folder.mkdir(parents=True, exist_ok=True)
        if git:
            self.git(folder, 'init', '-q')
        return folder

    def global_install(self, env):
        self.run_tool('install.py', '--runtime', 'claude', '--global', env=env)
        return Path(env['CLAUDE_CONFIG_DIR']) / 'skills'

    def test_project_install_uses_each_runtime_folder_and_stays_out_of_git_status(self):
        env = self.claude_env()
        project = self.project()
        result = json.loads(self.run_tool('install.py', '--runtime', 'claude', '--project',
                                          str(project), env=env).stdout)
        dest = project.resolve() / '.claude/skills'
        self.assertEqual(result['destination'], str(dest))
        self.assertEqual(result['project'], str(project.resolve()))
        self.assertEqual(result['git_exclude']['added'], 3)
        self.assertTrue((dest / 'coco-example/SKILL.md').is_file())
        self.assertFalse(Path(env['CLAUDE_CONFIG_DIR']).exists())
        self.assertEqual(self.git(project, 'status', '--porcelain', '--untracked-files=all'), '')
        self.run_tool('validate.py', '--installed', str(dest))
        again = json.loads(self.run_tool('install.py', '--runtime', 'claude', '--project',
                                         str(project), env=env).stdout)
        self.assertEqual((again['status'], again['git_exclude']['added']), ('unchanged', 0))
        self.run_tool('install.py', '--runtime', 'codex', '--project', str(project), env=env)
        self.assertTrue((project / '.agents/skills/coco-example/SKILL.md').is_file())
        self.assertEqual(self.git(project, 'status', '--porcelain', '--untracked-files=all'), '')

    def test_project_exclusions_are_repository_relative_and_leave_user_skills_visible(self):
        repo = self.project('repo')
        app = self.project('repo/apps/my app', git=False)
        own = app / '.claude/skills/team-skill/SKILL.md'
        own.parent.mkdir(parents=True)
        own.write_text('team-owned skill', encoding='utf-8')
        self.run_tool('install.py', '--runtime', 'claude', '--project', str(app),
                      env=self.claude_env())
        exclude = (repo / '.git/info/exclude').read_text(encoding='utf-8')
        self.assertIn('/apps/my app/.claude/skills/coco-example/\n', exclude)
        self.assertIn('/apps/my app/.claude/skills/.coco-install.*\n', exclude)
        self.assertEqual(self.git(repo, 'status', '--porcelain', '--untracked-files=all'),
                         '?? "apps/my app/.claude/skills/team-skill/SKILL.md"\n')

    def test_project_outside_git_installs_without_exclusions(self):
        project = self.project(git=False)
        result = json.loads(self.run_tool('install.py', '--runtime', 'claude', '--project',
                                          str(project), env=self.claude_env()).stdout)
        self.assertIsNone(result['git_exclude'])
        self.assertTrue((project / '.claude/skills/coco-example/SKILL.md').is_file())

    def test_several_projects_install_in_one_run(self):
        first, second = self.project('first'), self.project('second')
        results = json.loads(self.run_tool('install.py', '--runtime', 'claude', '--project',
                                           str(first), '--project', str(second),
                                           env=self.claude_env()).stdout)
        self.assertEqual([r['status'] for r in results], ['installed', 'installed'])
        for project in (first, second):
            self.assertTrue((project / '.claude/skills/coco-example/SKILL.md').is_file())

    def test_project_dry_run_writes_neither_files_nor_exclusions(self):
        env = self.claude_env()
        glob = self.global_install(env)
        project = self.project()
        exclude = project / '.git/info/exclude'
        before = exclude.read_text(encoding='utf-8') if exclude.exists() else None
        results = json.loads(self.run_tool('install.py', '--runtime', 'claude', '--project',
                                           str(project), '--remove-global', '--dry-run',
                                           env=env).stdout)
        self.assertEqual([r['status'] for r in results], ['dry-run', 'dry-run'])
        self.assertEqual(results[0]['git_exclude']['added'], 3)
        self.assertEqual(results[1]['action'], 'uninstall')
        self.assertFalse((project / '.claude').exists())
        self.assertEqual(exclude.read_text(encoding='utf-8') if exclude.exists() else None, before)
        self.run_tool('validate.py', '--installed', str(glob))

    def test_global_install_is_kept_with_a_warning_unless_removal_is_requested(self):
        env = self.claude_env()
        glob = self.global_install(env)
        result = self.run_tool('install.py', '--runtime', 'claude', '--project',
                               str(self.project()), env=env)
        self.assertIn('--remove-global', result.stderr)
        self.run_tool('validate.py', '--installed', str(glob))

    def test_remove_global_moves_an_existing_install_into_the_project(self):
        env = self.claude_env()
        glob = self.global_install(env)
        other = glob / 'unrelated/SKILL.md'
        other.parent.mkdir()
        other.write_text('user-owned unrelated skill', encoding='utf-8')
        project = self.project()
        results = json.loads(self.run_tool('install.py', '--runtime', 'claude', '--project',
                                           str(project), '--remove-global', env=env).stdout)
        self.assertEqual([r['status'] for r in results], ['installed', 'removed'])
        self.assertEqual(results[1]['destination'], str(glob))
        self.assertEqual(sorted(p.name for p in glob.iterdir()), ['unrelated'])
        self.assertEqual(other.read_text(encoding='utf-8'), 'user-owned unrelated skill')
        self.run_tool('validate.py', '--installed', str(project / '.claude/skills'))

    def test_modified_global_install_stops_removal_before_any_project_write(self):
        env = self.claude_env()
        glob = self.global_install(env)
        (glob / 'coco-example/SKILL.md').write_text('personal change', encoding='utf-8')
        project = self.project()
        result = self.run_tool('install.py', '--runtime', 'claude', '--project', str(project),
                               '--remove-global', env=env, expect=2)
        self.assertIn('Cannot remove the global install', result.stderr)
        self.assertFalse((project / '.claude').exists())
        self.assertEqual((glob / 'coco-example/SKILL.md').read_text(encoding='utf-8'), 'personal change')

    def test_project_and_removal_arguments_are_checked_before_writing(self):
        env = self.claude_env()
        self.run_tool('install.py', '--runtime', 'claude', '--project',
                      str(Path(self.temp.name) / 'missing'), env=env, expect=2)
        self.run_tool('install.py', '--runtime', 'claude', '--global', '--remove-global',
                      env=env, expect=2)
        self.run_tool('install.py', '--runtime', 'claude', '--global', '--project',
                      str(self.project()), env=env, expect=2)
        glob = self.global_install(env)
        self.run_tool('install.py', '--runtime', 'claude', '--dest', str(glob),
                      '--remove-global', env=env, expect=2)
        self.run_tool('install.py', '--uninstall', '--runtime', 'claude', '--remove-global',
                      env=env, expect=2)
        self.assertFalse((Path(self.temp.name) / 'missing').exists())
        self.run_tool('validate.py', '--installed', str(glob))
        with patch('install.Path.home', return_value=Path(self.temp.name)):
            with self.assertRaisesRegex(installer.PackageError, 'home folder'):
                installer.project_destination('claude', self.temp.name)

    def test_uninstall_removes_only_unmodified_managed_files(self):
        other = self.dest / 'unrelated/SKILL.md'
        other.parent.mkdir(parents=True)
        other.write_text('unrelated', encoding='utf-8')
        self.install()
        preview = json.loads(self.install('--uninstall', '--dry-run').stdout)
        self.assertEqual(preview['status'], 'dry-run')
        self.assertTrue((self.dest / 'coco-example/SKILL.md').is_file())
        (self.dest / 'coco-example/notes.txt').write_text('keep me', encoding='utf-8')
        self.install('--uninstall', expect=2)
        self.assertTrue((self.dest / 'coco-example/SKILL.md').is_file())
        (self.dest / 'coco-example/notes.txt').unlink()
        removed = json.loads(self.install('--uninstall').stdout)
        self.assertEqual((removed['status'], removed['files']), ('removed', 3))
        self.assertEqual(sorted(p.name for p in self.dest.iterdir()), ['unrelated'])
        self.assertEqual(json.loads(self.install('--uninstall').stdout)['status'], 'absent')

    def run_interactive(self, answers, *args, env):
        output = io.StringIO()
        argv = ['install.py', '--root', str(self.root), '--runtime', 'claude', *args]
        with patch.object(sys, 'argv', argv), patch.dict(os.environ, env), \
                patch('install.sys.stdin') as stdin, \
                patch('install.ask', side_effect=answers) as asked, redirect_stdout(output), \
                redirect_stderr(io.StringIO()):
            stdin.isatty.return_value = True
            installer.main()
        return json.loads(output.getvalue()), asked

    def test_terminal_prompt_chooses_projects_and_confirms_global_removal(self):
        env = self.claude_env()
        glob = self.global_install(env)
        first, second = self.project('first'), self.project('second')
        results, asked = self.run_interactive(['1', str(first), str(second), '', 'y'], env=env)
        self.assertEqual([r['status'] for r in results], ['installed', 'installed', 'removed'])
        self.assertIn('Remove it after the project install?', asked.call_args_list[-1].args[0])
        self.assertFalse((glob / '.coco-install.json').exists())
        for project in (first, second):
            self.run_tool('validate.py', '--installed', str(project / '.claude/skills'))

    def test_terminal_prompt_asks_again_instead_of_failing_on_a_bad_answer(self):
        env = self.claude_env()
        home, project = self.project('home', git=False), self.project()
        missing = Path(self.temp.name) / 'missing'
        with patch('install.Path.home', return_value=home), \
                patch('install.Path.cwd', return_value=home):
            result, asked = self.run_interactive(
                ['3', '1', '', str(home), str(missing), str(project), ''], env=env)
        self.assertEqual(result['project'], str(project.resolve()))
        prompts = [call.args[0] for call in asked.call_args_list]
        self.assertEqual(prompts[:3], ['Choose [1]: ', 'Choose 1 or 2: ', 'Project folder: '])
        self.assertEqual(prompts.count('Project folder: '), 4)
        self.assertFalse(missing.exists())

    def test_terminal_prompt_can_keep_or_choose_the_global_install(self):
        env = self.claude_env()
        glob = self.global_install(env)
        result, _ = self.run_interactive(['', str(self.project()), '', 'n'], env=env)
        self.assertEqual(result['status'], 'installed')
        self.run_tool('validate.py', '--installed', str(glob))
        result, asked = self.run_interactive(['2'], env=env)
        self.assertEqual((result['status'], result['destination']), ('unchanged', str(glob)))
        self.assertEqual(asked.call_count, 1)
        result, asked = self.run_interactive([], '--global', env=env)
        self.assertEqual(result['status'], 'unchanged')
        self.assertEqual(asked.call_count, 0)

    def test_symlink_in_package_or_target_is_refused(self):
        secret = Path(self.temp.name) / 'outside.txt'
        secret.write_text('external', encoding='utf-8')
        (self.root / 'skills/coco-example/link').symlink_to(secret)
        self.install(expect=2)
        self.assertFalse(self.dest.exists())
        (self.root / 'skills/coco-example/link').unlink()
        self.dest.symlink_to(self.root / 'skills', target_is_directory=True)
        self.install(expect=2)

    def test_manifest_cannot_escape_destination(self):
        config = json.loads((self.root / 'coco.json').read_text(encoding='utf-8'))
        config['skills'] = ['../outside']
        self.write('coco.json', json.dumps(config))
        self.install(expect=2)
        self.assertFalse(self.dest.exists())

    def test_broken_reference_and_wrong_name_are_rejected(self):
        self.write('skills/_coco-shared/contracts.md', '[bad](missing.md)\n')
        self.run_tool('validate.py', expect=2)
        self.write('skills/_coco-shared/contracts.md', '# Restored\n')
        p = self.root / 'skills/coco-example/SKILL.md'
        p.write_text(p.read_text(encoding='utf-8').replace('name: coco-example', 'name: wrong-name'))
        self.run_tool('validate.py', expect=2)

    def test_installed_tampering_is_detected(self):
        self.install()
        (self.dest / '_coco-shared/contracts.md').write_text('tampered', encoding='utf-8')
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
               'implemented_references': ['skills/coco-example/SKILL.md']}
        self.write('sources/coverage.json', json.dumps({'entries': [row]}))
        self.run_tool('validate.py')
        self.write('sources/a/SKILL.md.source', 'modified original')
        self.run_tool('validate.py', expect=2)
        self.write('sources/a/SKILL.md.source', raw.decode())
        self.write('sources/coverage.json', json.dumps({'entries': []}))
        self.run_tool('validate.py', expect=2)


if __name__ == '__main__':
    unittest.main()
