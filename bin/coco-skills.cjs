#!/usr/bin/env node
'use strict';

const { spawnSync } = require('node:child_process');
const path = require('node:path');
const { name, version } = require('../package.json');

const root = path.resolve(__dirname, '..');
const usage = `${name} ${version}

Usage:
  coco-skills install [--runtime codex|claude] [--project <folder>]... [--remove-global] [--dry-run]
  coco-skills install [--runtime codex|claude] --global [--dry-run]
  coco-skills install [--runtime codex|claude] --dest <directory> [--remove-global] [--dry-run]
  coco-skills uninstall [--runtime codex|claude] [--project <folder>... | --global | --dest <directory>] [--dry-run]
  coco-skills validate [--installed <directory>]
  coco-skills --version

Requires Python 3.9 or newer. Set COCO_PYTHON to a Python executable if needed.
Default runtime: codex. Claude Code: --runtime claude.
--project installs only for that project: <folder>/.claude/skills (Claude Code) or
<folder>/.agents/skills (Codex), hidden from Git through the project's .git/info/exclude.
--global installs for every project: $CLAUDE_CONFIG_DIR/skills (~/.claude/skills) or
$CODEX_HOME/skills (~/.codex/skills). An explicit --dest overrides both.
Without --project, --global or --dest, install asks in a terminal and installs globally otherwise.
--remove-global removes an existing global install once the project installs succeed.
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
  const scripts = {
    install: ['install.py'], uninstall: ['install.py', '--uninstall'], validate: ['validate.py'],
  };
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
  const [script, ...fixed] = scripts[command];
  const result = spawnSync(executable, [
    ...prefix, path.join(root, 'scripts', script), ...fixed, ...args,
  ], { env, stdio: 'inherit', windowsHide: true });
  if (result.error) {
    fail(`Could not start Python: ${result.error.message}`);
    return;
  }
  process.exitCode = result.status === null ? 1 : result.status;
}

main();
