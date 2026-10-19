"""Probe native Claude Code loading with localhost-only canned messages.

No model judgment is evaluated. The fake gateway chooses Read calls explicitly.
The report omits complete requests, system prompts, auth headers and local paths.
Use a preinstalled CLI; this script never downloads or installs Claude Code.
"""
import argparse
import http.server
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import threading


def string_values(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for child in value:
            yield from string_values(child)
    elif isinstance(value, dict):
        for child in value.values():
            yield from string_values(child)


def probe(cli, root):
    names = set(json.loads((root / 'coco.json').read_text())['skills'])
    version = subprocess.run([str(cli), '--version'], capture_output=True,
                             text=True, check=True, timeout=15).stdout.strip()
    with tempfile.TemporaryDirectory(prefix='coco-claude-native-') as td:
        scratch = Path(td).resolve()
        config = scratch / 'config'
        skills = config / 'skills'
        project = scratch / 'project'
        project.mkdir()
        env = {key: os.environ[key] for key in
               ['HOME', 'PATH', 'TMPDIR', 'USER', 'LANG', 'SHELL'] if key in os.environ}
        env.update({'CLAUDE_CONFIG_DIR': str(config), 'DISABLE_AUTOUPDATER': '1',
                    'CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC': '1',
                    'DISABLE_TELEMETRY': '1', 'DISABLE_ERROR_REPORTING': '1',
                    'NO_PROXY': '127.0.0.1,localhost'})
        subprocess.run([sys.executable, str(root / 'scripts/install.py'),
                        '--root', str(root), '--runtime', 'claude', '--dest', str(skills)],
                       capture_output=True, text=True, check=True, timeout=15)
        # A malformed control prevents a vacuous native-validator success claim.
        validation = {}
        control = scratch / 'control' / '.claude' / 'skills'
        shutil.copytree(skills, control)
        for label in ('valid', 'malformed'):
            if label == 'malformed':
                (control / 'coco-build' / 'SKILL.md').write_text(
                    '---\nname: [unterminated\ndescription: broken\n---\n# Invalid control\n')
            checked = subprocess.run([str(cli), 'plugin', 'validate', str(control),
                                      '--strict', '--json'], cwd=project, env=env,
                                     capture_output=True, text=True, timeout=15)
            try:
                data = json.loads(checked.stdout)
            except ValueError:
                data = {}
            validation[label] = {'exit': checked.returncode,
                                 'success': data.get('success'),
                                 'contents_count': len(data.get('contents', [])),
                                 'advice_count': len(data.get('advice', []))}
        validation['detects_malformed_control'] = (
            validation['valid']['exit'] == 0 and validation['malformed']['exit'] != 0)
        captured = []
        read_targets = {
            'contract': skills / '_coco-shared/contracts.md',
            'format': skills / 'coco-tellmeskill/references/explanation-format.md',
            'build': skills / 'coco-build/SKILL.md',
        }

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                captured.append({'path': self.path, 'body': body})
                if len(captured) == 1:
                    blocks = [{'type': 'tool_use', 'id': 'coco_' + key,
                               'name': 'Read', 'input': {'file_path': str(path)}}
                              for key, path in read_targets.items()]
                    reason = 'tool_use'
                else:
                    blocks = [{'type': 'text', 'text': 'Local loader probe complete.'}]
                    reason = 'end_turn'
                message = {'id': 'msg_coco_local_' + str(len(captured)),
                           'type': 'message', 'role': 'assistant',
                           'model': body.get('model', 'local-probe'), 'content': [],
                           'stop_reason': None, 'stop_sequence': None,
                           'usage': {'input_tokens': 1, 'output_tokens': 1}}
                events = [('message_start', {'type': 'message_start', 'message': message})]
                for index, block in enumerate(blocks):
                    initial = dict(block, input={}) if block['type'] == 'tool_use' else {'type': 'text', 'text': ''}
                    delta = ({'type': 'input_json_delta', 'partial_json': json.dumps(block['input'])}
                             if block['type'] == 'tool_use' else {'type': 'text_delta', 'text': block['text']})
                    events.extend([
                        ('content_block_start', {'type': 'content_block_start', 'index': index, 'content_block': initial}),
                        ('content_block_delta', {'type': 'content_block_delta', 'index': index, 'delta': delta}),
                        ('content_block_stop', {'type': 'content_block_stop', 'index': index})])
                events.extend([
                    ('message_delta', {'type': 'message_delta', 'delta': {'stop_reason': reason, 'stop_sequence': None}, 'usage': {'output_tokens': 1}}),
                    ('message_stop', {'type': 'message_stop'})])
                wire = ''.join('event: ' + kind + '\ndata: ' + json.dumps(data) + '\n\n'
                               for kind, data in events).encode()
                self.send_response(200)
                self.send_header('Content-Type', 'text/event-stream')
                self.send_header('Content-Length', str(len(wire)))
                self.end_headers()
                self.wfile.write(wire)

        server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        env.update({'ANTHROPIC_BASE_URL': 'http://127.0.0.1:' + str(server.server_address[1]),
                    'ANTHROPIC_API_KEY': 'coco-local-only-fake-key'})
        args = ['-p', '--verbose', '--output-format', 'stream-json',
                '--no-session-persistence', '--permission-mode', 'plan',
                '--strict-mcp-config', '--max-turns', '3', '--tools', 'Read,Skill', '--',
                '/coco-tellmeskill coco-build simple explanation']
        try:
            result = subprocess.run([str(cli), *args], cwd=project, env=env,
                                    capture_output=True, text=True, timeout=45)
        finally:
            server.shutdown()
        if result.returncode != 0:
            diagnostic = '\n'.join(line for line in result.stdout.splitlines() if '"type":"result"' in line or '"is_error":true' in line)
            raise AssertionError('Native CLI failed: ' + str(result.returncode) + ' ' + result.stderr[-500:] + diagnostic[-2000:])
        events = [json.loads(line) for line in result.stdout.splitlines() if line.startswith('{')]
        init = next(e for e in events if e.get('subtype') == 'init')
        final = next(e for e in events if e.get('type') == 'result')
        assert len(captured) == 2, 'Expected one loading request and one Read-result request'
        assert all(r['path'].split('?')[0] == '/v1/messages' for r in captured)
        first_texts = list(string_values(captured[0]['body']['messages']))
        first_text = '\n'.join(first_texts)
        loaded = set(re.findall(r'^- (coco-[a-z-]+):', first_text, re.M))
        assert loaded == names, 'Native catalog does not match coco.json'
        assert names <= set(init['skills']) and names <= set(init['slash_commands'])
        assert '<command-name>/coco-tellmeskill</command-name>' in first_text
        assert '<command-args>coco-build simple explanation</command-args>' in first_text
        source_body = (skills / 'coco-tellmeskill/SKILL.md').read_text().split('---\n', 2)[2].strip()
        assert source_body in first_text and 'ARGUMENTS: coco-build simple explanation' in first_text
        assert 'Base directory for this skill: ' in first_text
        results = {}
        for message in captured[1]['body']['messages']:
            content = message.get('content', [])
            if not isinstance(content, list):
                continue
            for block in content:
                if isinstance(block, dict) and block.get('type') == 'tool_result':
                    results[block['tool_use_id']] = block
        for key, path in read_targets.items():
            block = results['coco_' + key]
            assert not block.get('is_error', False), 'Read failed: ' + key
            actual = '\n'.join(string_values(block.get('content', '')))
            # Native Read adds line numbers; compare every nonempty source line.
            assert all(line in actual for line in path.read_text().splitlines() if line), key
        assert not final.get('permission_denials'), 'Read permission was denied'
        return {'claude_code_version': version, 'command': ['claude', *args],
                'installation': {'runtime': 'claude', 'skill_count': len(names), 'destination': '<isolated-config>/skills'},
                'native_loader': {'exit': result.returncode, 'catalog_names': sorted(loaded),
                                  'catalog_matches_manifest': True, 'slash_menu_contains_all': True,
                                  'selected_body_matches_source': True, 'arguments_loaded': True,
                                  'base_directory_provided': True},
                'native_reads': {'sibling_common_contract': True, 'own_supporting_file': True,
                                 'target_skill': True, 'permission_mode': 'plan', 'permission_denials': []},
                'transport': {'endpoint': 'localhost HTTP mock only', 'request_count': len(captured),
                              'credential': 'fake local-only key', 'real_model_api_calls': 0},
                'plugin_validator_negative_control': validation,
                'limitations': ['Canned responses choose the Read calls; model judgment and workflow compliance are not evaluated.',
                                'The CLI reports estimated model cost for canned token usage; no paid API was contacted.',
                                'Native plugin validation is not evidence of skill parsing when the malformed control is undetected.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cli', type=Path, required=True)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = probe(args.cli.resolve(), args.root.resolve())
    text = json.dumps(report, indent=2) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
