# Codex and Claude Code

COCO uses one maintained Agent Skills source tree for both runtimes. Keep each
`coco-*/SKILL.md`, its references, and the sibling `_coco-shared/` directory
together. Resolve relative links from the file containing them, not from the
project's working directory. `_coco-shared` is supporting material without a
`SKILL.md`; do not present it as an invocable skill.

| Runtime | Project destination | Global destination | Invocation |
| --- | --- | --- | --- |
| Codex | `<project>/.agents/skills` | `~/.codex/skills`, or `$CODEX_HOME/skills` when configured | `$coco-build <request>` |
| Claude Code | `<project>/.claude/skills` | `~/.claude/skills`, or `$CLAUDE_CONFIG_DIR/skills` when configured | `/coco-build <request>` |

Each runtime reads project skills from the folder a session starts in up to the
repository root, so `--project <folder>` limits COCO to that project. The
installer adds the installed folders to the project's `.git/info/exclude`
rather than the shared `.gitignore`. A global install applies to every project:
Claude Code runs a personal skill over a same-named project skill, and Codex
lists both, so a project install offers to remove an existing global install,
or does so with `--remove-global`. Explicit `--dest` overrides both
destinations. Install each runtime separately when both are used; updating one
directory does not update the other. The installer's default runtime remains
Codex for existing callers.

A terminal run without `--project`, `--global`, or `--dest` asks where to
install; any other run without them installs globally. An agent's shell is not
a terminal, so always pass the confirmed scope.

```sh
python3 scripts/install.py --runtime codex --project <project> --dry-run
python3 scripts/install.py --runtime codex --project <project>
python3 scripts/install.py --runtime claude --project <project> --dry-run
python3 scripts/install.py --runtime claude --project <project>
python3 scripts/install.py --runtime claude --global
python3 scripts/install.py --runtime claude --project <project> --remove-global
python3 scripts/install.py --runtime claude --uninstall --project <project>
python3 scripts/validate.py --installed <confirmed-skills-directory>
```

These commands run from the authoritative COCO repository. Use the supported
installer's ownership manifest and preservation checks for both runtimes. Do not
delete local changes, overwrite a foreign skill, or manufacture a manifest to
bypass a conflict. Skills do not install or authenticate the agent itself.

`name`, `description`, and `license` in `SKILL.md` are shared frontmatter.
`agents/openai.yaml` supplies Codex UI metadata; Claude Code discovers the skill
through `SKILL.md` and does not require that sidecar. Keep Codex metadata intact
when maintaining Claude Code support. No automatic tool grants, model selection,
or runtime-specific hook settings are added by installing this bundle.

Generate examples, explanations, and request options with the current runtime's
invocation syntax. For a namespaced external skill, retain its actual catalog
identifier instead of inventing a COCO alias. Invocation text belongs in the
agent's conversation, not in a shell. Do not treat a source example as permission
to execute its task. Question tools, independent agents, trackers, and browsers
remain conditional on what that runtime actually provides.

After installation, start a new agent session if the catalog has not refreshed.
In Claude Code, check the `/` menu and try a read-only explanation such as
`/coco-tellmeskill coco-build simple explanation`. Organizational settings can
restrict local skill loading. Native discovery and model behavior are separate
from file/hash validation; report what was actually checked.

This local installation supports Codex and Claude Code. It does not package the
bundle for claude.ai uploads or promise Claude Cowork/cloud session support.

## Shell commands

Check which shell runs your commands (bash, zsh, PowerShell or cmd) and write
for that shell. These rules keep the commands in COCO procedures working in all
of them:

- Brace a variable that a colon follows: `"${oid}:refs/heads/${branch}"` works
  in bash, zsh and PowerShell. zsh reads `$oid:r` as a modifier and PowerShell
  reads `$oid:refs` as a drive-qualified variable. In cmd write
  `"%OID%:refs/heads/%BRANCH%"`.
- Pass each branch name, path and message as one quoted argument: single quotes
  in bash, zsh and PowerShell, double quotes in cmd. Jira-derived branch names
  can contain parentheses and non-ASCII text.
- Join dependent commands with `&&` in bash, zsh, cmd and PowerShell 7. Windows
  PowerShell 5.1 has no `&&`; write `first; if ($LASTEXITCODE -eq 0) { second }`.
  Separate independent commands with `;`, or `&` in cmd.
- Never start a word with `=`, which zsh expands to a command path. Label output
  sections with a plain word such as `echo status:`. Quote arguments containing
  `*`, `?` or `[`, since zsh stops on an unmatched glob.
- Discard error output with `2>/dev/null` in bash and zsh, `2>$null` in
  PowerShell and `2>nul` in cmd.
- Windows shells lack `head`, `grep`, `sed` and `xargs`. Prefer Git's own options
  (`--format`, `-n`, `--porcelain`, `--name-only`, `git grep`) and the bundled
  Python helpers.
- Where a procedure says `python3`, use the interpreter that exists: `COCO_PYTHON`
  when set, otherwise `python3`, `python`, then `py -3` on Windows.
- Before reading Git output with non-ASCII text such as Korean branch names or
  paths, run Git with `-c core.quotepath=false`; in Windows PowerShell 5.1 also
  set `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8`, and in cmd run
  `chcp 65001`.

Official Claude Code references:
[skill discovery, invocation, and supporting files](https://code.claude.com/docs/en/skills)
and [configuration directories](https://code.claude.com/docs/en/settings).
Codex reference: [where Codex loads local skills](https://learn.chatgpt.com/docs/build-skills).
