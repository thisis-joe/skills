"""Run the coco-tellmeskill recent-skill helper on runtime-shaped session records."""
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/coco-tellmeskill'
HELPER = SKILL / 'tools/recent_skills.py'
GROUPS = SKILL / 'references/skill-groups.md'
NOW = datetime.now(timezone.utc)
SECRET = 'PRIVATE-PROMPT-TEXT'


def stamp(days_ago, minutes=0):
    moment = NOW - timedelta(days=days_ago, minutes=minutes)
    return moment.strftime('%Y-%m-%dT%H:%M:%S.') + '%03dZ' % (moment.microsecond // 1000)


def claude_tool_use(skill, when):
    return {'type': 'assistant', 'timestamp': when, 'message': {'role': 'assistant', 'content': [
        {'type': 'text', 'text': 'Loading the skill.'},
        {'type': 'tool_use', 'id': 'toolu_1', 'name': 'Skill',
         'input': {'skill': skill, 'args': SECRET}}]}}


def claude_command(command, when, as_list=False):
    text = (f'<command-message>{command}</command-message>\n'
            f'<command-name>/{command}</command-name>\n<command-args>{SECRET}</command-args>')
    content = [{'type': 'text', 'text': text}] if as_list else text
    return {'type': 'user', 'timestamp': when, 'message': {'role': 'user', 'content': content}}


def codex_meta(cwd, when):
    return {'timestamp': when, 'type': 'session_meta',
            'payload': {'id': 'session', 'cwd': str(cwd), 'base_instructions': SECRET}}


def codex_selected(skill, when):
    text = f'<skill>\n<name>{skill}</name>\n<path>/skills/{skill}/SKILL.md</path>\n{SECRET}\n</skill>'
    return {'timestamp': when, 'type': 'response_item', 'payload': {
        'type': 'message', 'role': 'user', 'content': [{'type': 'input_text', 'text': text}],
        'internal_chat_message_metadata_passthrough': {
            'content_item_kinds': ['skills.selected_skill_instructions']}}}


def write_jsonl(path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as handle:
        for record in records:
            handle.write((record if isinstance(record, str) else json.dumps(record)) + '\n')


def claude_slug(path):
    return re.sub(r'[^A-Za-z0-9]', '-', str(path))


class RecentSkillTests(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.base = Path(scratch.name).resolve()
        self.workspace = self.base / 'work' / 'my.app'
        self.workspace.mkdir(parents=True)
        self.claude = self.base / 'claude-config'
        self.codex = self.base / 'codex-home'

    def run_helper(self, *args, env=None, cwd=None):
        environment = {key: value for key, value in os.environ.items()
                       if key not in ('CLAUDE_CONFIG_DIR', 'CODEX_HOME')}
        environment.update(env or {})
        result = subprocess.run(
            [sys.executable, str(HELPER), *args], cwd=cwd or self.workspace, env=environment,
            capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn(SECRET, result.stdout)
        return json.loads(result.stdout)

    def names(self, report):
        return [entry['name'] for entry in report['skills']]

    def claude_project(self, workspace=None, suffix=''):
        return self.claude / 'projects' / (claude_slug(workspace or self.workspace) + suffix)

    def test_claude_lists_latest_distinct_skills_for_this_workspace_only(self):
        project = self.claude_project()
        write_jsonl(project / 'older.jsonl', [
            claude_tool_use('coco-build', stamp(5)),
            claude_command('coco-review', stamp(4)),
            claude_tool_use('coco-build', stamp(3)),
            'not json, ignored',
        ])
        write_jsonl(project / 'newer.jsonl', [
            claude_command('coco-verify', stamp(1), as_list=True),
            claude_tool_use('plugin-name:helper', stamp(2)),
            claude_command('model', stamp(0, 5)),
            claude_tool_use('coco-tellmeskill', stamp(0, 1)),
        ])
        write_jsonl(project / 'session-id' / 'subagents' / 'agent.jsonl', [
            claude_tool_use('coco-security', stamp(0, 2))])
        write_jsonl(self.claude_project(suffix='--claude-worktrees-feature') / 'w.jsonl', [
            claude_tool_use('coco-plan', stamp(2, 30))])
        write_jsonl(self.claude_project(self.base / 'work' / 'other') / 'x.jsonl', [
            claude_tool_use('coco-ship', stamp(0, 3))])
        write_jsonl(self.claude_project(suffix='-sibling') / 'y.jsonl', [
            claude_tool_use('coco-debug', stamp(0, 4))])

        report = self.run_helper(
            '--runtime', 'claude', '--limit', '10', '--exclude', 'coco-tellmeskill',
            '--available', 'coco-build,coco-review,coco-verify,coco-plan,coco-ship,coco-debug',
            '--available', 'plugin-name:helper,coco-security,coco-tellmeskill',
            env={'CLAUDE_CONFIG_DIR': str(self.claude)})

        self.assertEqual(self.names(report), [
            'coco-verify', 'plugin-name:helper', 'coco-plan', 'coco-build', 'coco-review'])
        self.assertEqual(report['skills'][3]['last_used'], stamp(3))
        self.assertEqual(report['workspace'], str(self.workspace))

    def test_default_limit_is_three_and_unfiltered_markers_stay_identifiers(self):
        write_jsonl(self.claude_project() / 's.jsonl', [
            claude_tool_use('coco-build', stamp(4)),
            claude_tool_use('coco-review', stamp(3)),
            claude_command('product:brainstorm', stamp(2)),
            claude_tool_use('coco-verify', stamp(1)),
        ])
        report = self.run_helper('--runtime', 'claude', '--config-dir', str(self.claude))
        self.assertEqual(self.names(report), ['coco-verify', 'product:brainstorm', 'coco-review'])

    def test_events_older_than_the_window_are_ignored(self):
        write_jsonl(self.claude_project() / 's.jsonl', [
            claude_tool_use('coco-build', stamp(40)),
            claude_tool_use('coco-review', stamp(10)),
        ])
        default = self.run_helper('--runtime', 'claude', '--config-dir', str(self.claude))
        narrow = self.run_helper('--runtime', 'claude', '--config-dir', str(self.claude),
                                 '--days', '7')
        self.assertEqual(self.names(default), ['coco-review'])
        self.assertEqual(default['days'], 30)
        self.assertEqual(self.names(narrow), [])

    def test_codex_reads_only_sessions_started_in_this_workspace(self):
        day = self.codex / 'sessions' / '2026' / '10' / '20'
        write_jsonl(day / 'rollout-a.jsonl', [
            codex_meta(self.workspace, stamp(3)),
            codex_selected('coco-build', stamp(3)),
            codex_selected('superpowers:writing-plans', stamp(1)),
        ])
        write_jsonl(day / 'rollout-b.jsonl', [
            codex_meta(self.workspace / 'packages' / 'api', stamp(2)),
            codex_selected('coco-review', stamp(2)),
        ])
        write_jsonl(day / 'rollout-c.jsonl', [
            codex_meta(self.base / 'work' / 'my.app-other', stamp(0)),
            codex_selected('coco-ship', stamp(0)),
        ])
        write_jsonl(day / 'rollout-d.jsonl', [codex_selected('coco-debug', stamp(0))])

        report = self.run_helper('--runtime', 'codex', '--limit', '5',
                                 env={'CODEX_HOME': str(self.codex)})

        self.assertEqual(self.names(report),
                         ['superpowers:writing-plans', 'coco-review', 'coco-build'])

    def test_missing_records_return_an_empty_list(self):
        for runtime in ('claude', 'codex'):
            report = self.run_helper('--runtime', runtime, '--config-dir',
                                     str(self.base / 'missing'))
            self.assertEqual(report['skills'], [])

    def test_explicit_workspace_overrides_the_current_directory(self):
        write_jsonl(self.claude_project() / 's.jsonl', [claude_tool_use('coco-build', stamp(1))])
        report = self.run_helper('--runtime', 'claude', '--config-dir', str(self.claude),
                                 '--workspace', str(self.workspace), cwd=self.base)
        self.assertEqual(self.names(report), ['coco-build'])

    def test_documented_invocation_runs_against_runtime_records(self):
        text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        commands = re.findall(r'`(python3 tools/recent_skills\.py [^`]+)`', text)
        self.assertEqual(len(commands), 1, 'SKILL.md documents exactly one helper command')
        write_jsonl(self.claude_project() / 's.jsonl', [
            claude_tool_use('coco-build', stamp(2)),
            claude_tool_use('coco-tellmeskill', stamp(1)),
            claude_command('model', stamp(0, 1)),
        ])
        argv = shlex.split(commands[0])[2:]
        replacements = {'<claude|codex>': 'claude', '<project-directory>': str(self.workspace),
                        '<catalog-identifiers>': 'coco-build,coco-tellmeskill'}
        argv = [replacements.get(arg, arg) for arg in argv]
        self.assertFalse([arg for arg in argv if arg.startswith('<')], argv)
        report = self.run_helper(*argv, env={'CLAUDE_CONFIG_DIR': str(self.claude)})
        self.assertEqual(self.names(report), ['coco-build'])


class SkillGroupTests(unittest.TestCase):
    def test_every_group_has_a_description_and_classification_criteria(self):
        text = GROUPS.read_text(encoding='utf-8')
        rows = re.findall(r'^\| \*\*(.+?)\*\* \| (.+?) \| (.+?) \|$', text, re.M)
        self.assertGreaterEqual(len(rows), 5)
        self.assertEqual(rows[-1][0], 'Other')
        for name, description, criteria in rows:
            self.assertGreater(len(description.split()), 4, name)
            self.assertGreater(len(criteria.split()), 2, name)

    def test_skill_links_the_group_reference_and_recent_first_flow(self):
        text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('(references/skill-groups.md)', text)
        self.assertIn('tools/recent_skills.py', text)


if __name__ == '__main__':
    unittest.main()
