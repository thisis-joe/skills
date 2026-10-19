# Codex and Claude Code

COCO uses one maintained Agent Skills source tree for both runtimes. Keep each
`coco-*/SKILL.md`, its references, and the sibling `_coco-shared/` directory
together. Resolve relative links from the file containing them, not from the
project's working directory. `_coco-shared` is supporting material without a
`SKILL.md`; do not present it as an invocable skill.

| Runtime | Personal destination | Invocation |
| --- | --- | --- |
| Codex | `~/.codex/skills`, or `$CODEX_HOME/skills` when configured | `$coco-build <request>` |
| Claude Code | `~/.claude/skills`, or `$CLAUDE_CONFIG_DIR/skills` when configured | `/coco-build <request>` |

For Claude Code project scope, install the whole bundle in the target project's
`.claude/skills/`. Explicit `--dest` overrides the personal destination. Install
each runtime separately when both are used; updating one directory does not
update the other. The installer's default remains Codex for existing callers.

```sh
python3 scripts/install.py --runtime codex --dry-run
python3 scripts/install.py --runtime codex
python3 scripts/install.py --runtime claude --dry-run
python3 scripts/install.py --runtime claude
python3 scripts/install.py --runtime claude --dest /project/.claude/skills
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

Official Claude Code references:
[skill discovery, invocation, and supporting files](https://code.claude.com/docs/en/skills)
and [configuration directories](https://code.claude.com/docs/en/settings).
