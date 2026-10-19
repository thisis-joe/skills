#!/usr/bin/env node
'use strict';

const { spawnSync } = require('node:child_process');
const path = require('node:path');
const { name, version } = require('../package.json');

const root = path.resolve(__dirname, '..');
const usage = `${name} ${version}

Usage:
  coco-skills install [--runtime codex|claude] [--dest <directory>] [--dry-run]
  coco-skills validate [--installed <directory>]
  coco-skills --version

Requires Python 3.9 or newer. Set COCO_PYTHON to a Python executable if needed.
Default runtime: codex ($CODEX_HOME/skills or ~/.codex/skills).
Claude Code: --runtime claude ($CLAUDE_CONFIG_DIR/skills or ~/.claude/skills).
An explicit --dest overrides either runtime's default directory.
Updates use the same install command and preserve locally modified files.
`;

function fail(message) {
  process.stderr.write(`${message}\n`);
  process.exitCode = 2;
}

function main() {
  const [command, ...args] = process.argv.slice(2);
  if (!command || command === '--help' || command === '-h' || command === 'help') {
    process.stdout.write(usage);
    return;
  }
  if (command === '--version' || command === '-v') {
    process.stdout.write(`${version}\n`);
    return;
  }
  const scripts = { install: 'install.py', validate: 'validate.py' };
  if (!Object.hasOwn(scripts, command)) {
    fail(`Unknown command: ${command}\n\n${usage}`);
    return;
  }
  if (args.includes('--help') || args.includes('-h')) {
    process.stdout.write(usage);
    return;
  }

  // Probe before running the installer, then execute its mutation exactly once.
  const env = { ...process.env, PYTHONUTF8: '1', PYTHONDONTWRITEBYTECODE: '1' };
  const candidates = process.env.COCO_PYTHON
    ? [[process.env.COCO_PYTHON, []]]
    : [['python3', []], ['python', []], ['py', ['-3']]];
  const python = candidates.find(([executable, prefix]) => {
    const result = spawnSync(executable, [...prefix, '-c',
      'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)'], {
      env, stdio: 'ignore', timeout: 5000, windowsHide: true,
    });
    return !result.error && result.status === 0;
  });
  if (!python) {
    fail('Python 3.9 or newer is required. Install Python or set COCO_PYTHON to its executable path.');
    return;
  }

  const [executable, prefix] = python;
  const result = spawnSync(executable, [
    ...prefix, path.join(root, 'scripts', scripts[command]), ...args,
  ], { env, stdio: 'inherit', windowsHide: true });
  if (result.error) {
    fail(`Could not start Python: ${result.error.message}`);
    return;
  }
  process.exitCode = result.status === null ? 1 : result.status;
}

main();
