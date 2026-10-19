# Codex and Claude Code support

The user requires **both** runtimes. Claude Code support is additive: the
default `scripts/install.py` invocation still installs for Codex, and the same
maintained skill payload is installed for either runtime. Implementation commit:
`9290beba31c951d1972425a22bf5d544cc81c475`, based on
`1b796d42f20373914dc64883ab6996b844c68a5e`, on
`feat/coco-claude-code-support`. No Jira task was supplied for this repository
maintenance request; no task number or Summary was invented.

## Changes and preserved behavior

- `--runtime codex|claude` selects the personal destination. Codex remains the
  default; Claude Code uses `~/.claude/skills` or `$CLAUDE_CONFIG_DIR/skills`.
- Explicit `--dest` still wins, including project `.claude/skills` installs.
  The ownership manifest, preflight checks, staging, and recovery code are
  unchanged. Foreign skills and personal modifications remain protected.
- The common contract and invocation-producing procedures use `$name` in Codex
  and `/name` in Claude Code. Codex UI sidecars remain unchanged. Both runtimes
  use the same `SKILL.md`, references, and sibling `_coco-shared` directory.
- README documents both runtimes and all 26 paired invocations. `CLAUDE.md`
  imports `AGENTS.md` so repository rules have one owner, including on clients
  that do not load `AGENTS.md` directly.
- The runtime choice and reason are recorded in the existing integration
  decisions. Frozen upstream sources, checksums, coverage facts, and historical
  evaluation records were not rewritten.

## Observed checks

The new CLI acceptance tests first failed because `--runtime` was unrecognized.
After implementation, package validation and all **48 tests** passed. The seven
added tests cover default destinations, configured Claude installation and
idempotency, dry-run without writes, project destination precedence, independent
Codex/Claude installs, modified/unrelated-file preservation, and invalid runtime
rejection. Existing tests retain source traceability and installation safeguards.

[installation.json](installation.json) records actual installation in both
personal destinations, repeated `unchanged` results, validation, source hashes,
and unrelated-file aggregate hashes. Each installed bundle contains 26 skills
and 100 files, byte-identical to the maintained source. All 50 unrelated Codex
files were preserved; the Claude skills directory had no unrelated files.

[checks.json](checks.json) pins the implementation files and verification
results. [review.md](review.md) records the independent implementation review and
its limits. Native client loader evidence is recorded separately from the
repository checks and from live model behavior.

## Native Claude Code loader with a mocked model

[native-loader.json](native-loader.json) records a successful run of the actual
Claude Code **2.1.303** client. An isolated installation was created through the
supported installer. The client reported all 26 COCO skills and slash commands,
loaded the exact selected `coco-tellmeskill` body and its arguments, and supplied
the installed base directory. Native `Read` tool results contained the actual
sibling common contract, the skill's explanation format, and `coco-build` source,
with no permission denials in normal `plan` mode.

The model transport was a localhost HTTP stub with a fixed fake key and canned
responses that explicitly selected those three reads. Two messages requests
were observed. This proves native discovery, slash invocation, argument loading,
and file access; it does **not** prove that a real model will choose those reads,
follow the explanation format, or comply with every workflow. No live model
response is represented as tested.

The `plugin validate` negative control accepted both a valid and a deliberately
malformed skill with empty component results. Its successful exit was therefore
excluded as evidence of skill parsing, and the suggested README command was
removed. The meaningful native evidence comes from the loader/tool roundtrip.

Reproduce with an already installed Claude Code CLI:

```sh
python3 docs/evaluation/dual-runtime/claude_native_loader_probe.py \
  --cli /path/to/claude --root . --output /tmp/coco-native-loader.json
```

The harness uses temporary installation/config/project directories, excludes
real authentication environment variables, points model requests at localhost,
limits runtime, and cleans up its temporary fixtures. Assertions fail on missing
catalog entries, incorrect invocation/body/arguments, denied or incomplete reads,
or unexpected request counts. Its report omits raw requests, system prompts,
debug logs, and local temporary paths. Installing the CLI is separate from this
script and from the COCO package installer.

## Support boundaries and sources

The package installs skills rather than the coding agents or their credentials.
Native model judgment, every workflow branch, organizational loading policies,
and all client versions are not certified by file validation. This work does
not package standalone uploads for claude.ai or promise Cowork support.

Official sources checked on 2026-10-19:

- [Claude Code skills](https://code.claude.com/docs/en/skills): personal/project
  locations, `/name` invocation, frontmatter, and supporting files.
- [Claude Code settings](https://code.claude.com/docs/en/settings): alternate
  personal configuration directory.
- [Claude Code project memory](https://code.claude.com/docs/en/memory):
  `CLAUDE.md` imports and shared repository instructions.
- [Claude Code CLI](https://code.claude.com/docs/en/cli-reference) and
  [setup](https://code.claude.com/docs/en/setup): native verification commands
  and disposable npm installation of the official client.
