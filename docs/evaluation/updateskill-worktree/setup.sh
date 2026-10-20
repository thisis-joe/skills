#!/bin/bash
# Build three isolated fixtures from the candidate package; no global Git config.
set -euo pipefail
SRC="$1"; OUT="$2"
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
rm -rf "$OUT"; mkdir -p "$OUT"
for c in write proposal nogit; do
  F="$OUT/$c"; mkdir -p "$F/repo"
  (cd "$SRC" && git ls-files -z | rsync -a --from0 --files-from=- ./ "$F/repo/")
  python3 "$F/repo/scripts/install.py" --root "$F/repo" --dest "$F/installed" >/dev/null
  if [ "$c" != nogit ]; then
    git -C "$F/repo" init -q -b main
    git -C "$F/repo" config user.email fixture@example.test
    git -C "$F/repo" config user.name Fixture
    git -C "$F/repo" add -A && git -C "$F/repo" commit -qm "baseline package"
    git -C "$F/repo" switch -qc feat/unrelated-work
    echo "unrelated" > "$F/repo/docs/unrelated.md"
    git -C "$F/repo" add docs/unrelated.md && git -C "$F/repo" commit -qm "docs: unrelated work"
    printf '\nPersonal uncommitted note.\n' >> "$F/repo/README.md"
    echo "scratch" > "$F/repo/scratch-notes.txt"
  fi
  (cd "$F/repo" && find . -path ./.git -prune -o -type f -print0 | sort -z | xargs -0 shasum -a 256) > "$F/before-files.sha256"
  if [ "$c" != nogit ]; then
    { git -C "$F/repo" branch --show-current; git -C "$F/repo" rev-parse HEAD; git -C "$F/repo" status --porcelain; git -C "$F/repo" worktree list --porcelain; git -C "$F/repo" branch --list; } > "$F/before-git.txt"
  fi
  (cd "$F/installed" && find . -type f -print0 | sort -z | xargs -0 shasum -a 256) > "$F/before-installed.sha256"
done
