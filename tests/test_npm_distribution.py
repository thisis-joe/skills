"""Exercise the published archive through npm, outside the source checkout."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
NODE = shutil.which('node')
NPM = shutil.which('npm')


@unittest.skipUnless(NODE and NPM, 'Node.js and npm are needed for distribution tests')
class NpmDistributionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='coco-npm-test-')
        cls.addClassCleanup(cls.temp.cleanup)
        cls.scratch = Path(cls.temp.name)
        cls.env = dict(os.environ, COCO_PYTHON=sys.executable,
                       npm_config_cache=str(cls.scratch / 'npm-cache'),
                       npm_config_offline='true', npm_config_audit='false',
                       npm_config_fund='false', npm_config_update_notifier='false')
        # `npm publish --dry-run` exports this to prepack; it would stop our own pack writing an archive.
        cls.env.pop('npm_config_dry_run', None)
        result = subprocess.run(
            [NPM, 'pack', '--ignore-scripts', '--json', '--pack-destination', str(cls.scratch)],
            cwd=ROOT, env=cls.env, capture_output=True, text=True, encoding='utf-8')
        if result.returncode:
            raise AssertionError(result.stdout + result.stderr)
        cls.archive_info = json.loads(result.stdout)[0]
        cls.archive = cls.scratch / cls.archive_info['filename']
        with tarfile.open(cls.archive) as archive:
            # The archive is our own output; still reject unexpected extraction paths.
            for member in archive.getmembers():
                target = (cls.scratch / member.name).resolve()
                if not target.is_relative_to(cls.scratch.resolve()) or not member.isfile():
                    raise AssertionError('Unexpected archive member: ' + member.name)
            archive.extractall(cls.scratch)
        cls.package = cls.scratch / 'package'

    def setUp(self):
        self.work = Path(tempfile.mkdtemp(dir=self.scratch))
        self.dest = self.work / '설치 경로 with spaces'
        self.cli = self.package / 'bin/coco-skills.cjs'

    def run_cli(self, *args, expect=0, env=None):
        result = subprocess.run([NODE, str(self.cli), *map(str, args)],
                                cwd=self.work, env=env or self.env, stdin=subprocess.DEVNULL,
                                capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, expect, result.stdout + result.stderr)
        return result

    def test_archive_contains_complete_bundle_and_provenance_only(self):
        paths = {item['path'] for item in self.archive_info['files']}
        self.assertIn('LICENSE', paths)
        self.assertIn('THIRD_PARTY_NOTICES.md', paths)
        self.assertIn('sources/manifest.json', paths)
        self.assertIn('sources/coverage.json', paths)
        self.assertIn('skills/_coco-shared/contracts.md', paths)
        allowed_files = {'package.json', 'README.md', 'LICENSE', 'THIRD_PARTY_NOTICES.md',
                         'coco.json', 'scripts/install.py', 'scripts/package_utils.py',
                         'scripts/validate.py', 'docs/distribution.md', 'docs/coco-1.2.0.md', 'docs/design.md',
                         'docs/implementation-plan.md', 'docs/source-index.md'}
        for path in paths:
            self.assertTrue(path in allowed_files or path.startswith(
                ('bin/', 'skills/', 'sources/')), path)
            self.assertNotIn('__pycache__', path)
        self.assertIn('Validated package:', self.run_cli('validate').stdout)

    def test_npm_exec_installs_archive_without_checkout_or_registry_access(self):
        preview = subprocess.run(
            [NPM, 'exec', '--yes', '--offline', '--ignore-scripts', '--',
             'file:' + str(self.archive), 'install', '--dry-run', '--dest', str(self.dest)],
            cwd=self.work, env=self.env, stdin=subprocess.DEVNULL,
            capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)
        self.assertEqual(json.loads(preview.stdout)['status'], 'dry-run')
        self.assertFalse(self.dest.exists())
        result = subprocess.run(
            [NPM, 'exec', '--yes', '--offline', '--ignore-scripts',
             '--package=' + str(self.archive), '--', 'coco-skills',
             'install', '--dest', str(self.dest)],
            cwd=self.work, env=self.env, stdin=subprocess.DEVNULL,
            capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)['status'], 'installed')
        data = json.loads((self.package / 'coco.json').read_text(encoding='utf-8'))
        for name in data['skills']:
            self.assertTrue((self.dest / name / 'SKILL.md').is_file())
        self.assertFalse((self.dest / 'sources').exists())
        self.assertIn('Validated installed bundle:', self.run_cli(
            'validate', '--installed', self.dest).stdout)

    def test_dry_run_has_no_filesystem_effect(self):
        result = self.run_cli('install', '--dry-run', '--dest', self.dest)
        self.assertEqual(json.loads(result.stdout)['status'], 'dry-run')
        self.assertFalse(self.dest.exists())

    def test_reinstall_is_unchanged_and_preserves_unrelated_skills(self):
        other = self.dest / 'unrelated/SKILL.md'
        other.parent.mkdir(parents=True)
        other.write_text('User skill', encoding='utf-8')
        self.run_cli('install', '--dest', self.dest)
        result = self.run_cli('install', '--dest', self.dest)
        self.assertEqual(json.loads(result.stdout)['status'], 'unchanged')
        self.assertEqual(other.read_text(encoding='utf-8'), 'User skill')

    def test_foreign_skill_failure_reaches_npm_cli_without_partial_install(self):
        name = json.loads((self.package / 'coco.json').read_text(encoding='utf-8'))['skills'][0]
        target = self.dest / name / 'SKILL.md'
        target.parent.mkdir(parents=True)
        target.write_text('User skill', encoding='utf-8')
        result = self.run_cli('install', '--dest', self.dest, expect=2)
        self.assertIn('Foreign skill directory', result.stderr)
        self.assertEqual(target.read_text(encoding='utf-8'), 'User skill')
        self.assertFalse((self.dest / '_coco-shared').exists())

    def test_help_version_and_unknown_command_do_not_require_python(self):
        env = dict(self.env, COCO_PYTHON=str(self.work / 'missing-python'))
        package = json.loads((self.package / 'package.json').read_text(encoding='utf-8'))
        usage = self.run_cli('--help', env=env).stdout
        for word in ('install', 'uninstall', '--project', '--global', '--remove-global'):
            self.assertIn(word, usage)
        self.assertIn('install', self.run_cli(env=env).stdout)
        self.assertEqual(self.run_cli('--version', env=env).stdout.strip(), package['version'])
        self.assertIn('Unknown command', self.run_cli('unknown', env=env, expect=2).stderr)

    def test_missing_python_reports_requirement_and_does_not_install(self):
        env = dict(self.env, COCO_PYTHON=str(self.work / 'missing-python'))
        result = self.run_cli('install', '--dest', self.dest, env=env, expect=2)
        self.assertIn('Python 3.9', result.stderr)
        self.assertIn('COCO_PYTHON', result.stderr)
        self.assertFalse(self.dest.exists())

    def test_python_is_discovered_without_an_explicit_override(self):
        env = {key: value for key, value in self.env.items() if key != 'COCO_PYTHON'}
        self.assertIn('Validated package:', self.run_cli('validate', env=env).stdout)

    def test_codex_home_selects_default_destination(self):
        codex_home = self.work / 'codex home'
        env = dict(self.env, CODEX_HOME=str(codex_home))
        result = self.run_cli('install', '--dry-run', env=env)
        self.assertEqual(json.loads(result.stdout)['destination'], str(codex_home / 'skills'))
        self.assertFalse(codex_home.exists())

    def test_claude_runtime_uses_its_config_even_with_codex_home(self):
        claude_config = self.work / 'claude config'
        codex_config = self.work / 'codex config'
        env = dict(self.env, CLAUDE_CONFIG_DIR=str(claude_config), CODEX_HOME=str(codex_config))
        result = self.run_cli('install', '--runtime=claude', env=env)
        self.assertEqual(json.loads(result.stdout)['destination'], str(claude_config / 'skills'))
        self.assertFalse(codex_config.exists())
        self.assertTrue((claude_config / 'skills/_coco-shared/runtimes.md').is_file())
        self.assertIn('Validated installed bundle:', self.run_cli(
            'validate', '--installed', claude_config / 'skills', env=env).stdout)
        again = self.run_cli('install', '--runtime', 'claude', env=env)
        self.assertEqual(json.loads(again.stdout)['status'], 'unchanged')

    def test_explicit_destination_beats_runtime_and_both_config_homes(self):
        env = dict(self.env, CODEX_HOME=str(self.work / 'codex'),
                   CLAUDE_CONFIG_DIR=str(self.work / 'claude'))
        self.run_cli('install', '--runtime', 'claude', '--dest', self.dest, env=env)
        self.assertTrue((self.dest / 'coco-build/SKILL.md').is_file())
        self.assertFalse((self.work / 'codex').exists())
        self.assertFalse((self.work / 'claude').exists())

    def test_npm_exec_claude_install_uses_the_published_archive(self):
        env = dict(self.env, CLAUDE_CONFIG_DIR=str(self.work / 'claude'),
                   CODEX_HOME=str(self.work / 'codex'))
        result = subprocess.run(
            [NPM, 'exec', '--yes', '--offline', '--ignore-scripts',
             '--package=' + str(self.archive), '--', 'coco-skills',
             'install', '--runtime', 'claude'], cwd=self.work, env=env,
            stdin=subprocess.DEVNULL, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)['destination'], str(self.work / 'claude/skills'))
        self.assertFalse((self.work / 'codex').exists())
        self.assertIn('Validated installed bundle:', self.run_cli(
            'validate', '--installed', self.work / 'claude/skills', env=env).stdout)

    def test_unknown_runtime_does_not_write_either_config_directory(self):
        env = dict(self.env, CLAUDE_CONFIG_DIR=str(self.work / 'claude'),
                   CODEX_HOME=str(self.work / 'codex'))
        self.run_cli('install', '--runtime', 'invalid', env=env, expect=2)
        self.assertFalse((self.work / 'codex').exists())
        self.assertFalse((self.work / 'claude').exists())


    def test_project_install_replaces_global_install_and_uninstall_reaches_python(self):
        env = dict(self.env, CLAUDE_CONFIG_DIR=str(self.work / 'claude'),
                   CODEX_HOME=str(self.work / 'codex'))
        glob = self.work / 'claude/skills'
        self.run_cli('install', '--runtime', 'claude', '--global', env=env)
        project = self.work / '프로젝트 with spaces'
        project.mkdir()
        subprocess.run(['git', 'init', '-q', str(project)], check=True)
        results = json.loads(self.run_cli('install', '--runtime', 'claude', '--project', project,
                                          '--remove-global', env=env).stdout)
        self.assertEqual([r['status'] for r in results], ['installed', 'removed'])
        self.assertFalse((glob / '.coco-install.json').exists())
        status = subprocess.run(['git', '-C', str(project), 'status', '--porcelain',
                                 '--untracked-files=all'], capture_output=True, text=True,
                                encoding='utf-8', check=True)
        self.assertEqual(status.stdout, '')
        self.assertIn('Validated installed bundle:', self.run_cli(
            'validate', '--installed', project / '.claude/skills', env=env).stdout)
        removed = json.loads(self.run_cli('uninstall', '--runtime', 'claude', '--project',
                                          project, env=env).stdout)
        self.assertEqual((removed['status'], removed['action']), ('removed', 'uninstall'))
        self.assertFalse((project / '.claude/skills/coco-build').exists())

if __name__ == '__main__':
    unittest.main()
