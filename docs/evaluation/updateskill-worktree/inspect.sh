#!/bin/bash
# Compare a fixture's starting checkout, worktrees and installation with its recorded baseline.
set -uo pipefail
F="$1"
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
echo "== $F"
(cd "$F/repo" && find . -path ./.git -prune -o -type f -print0 | sort -z | xargs -0 shasum -a 256) > "$F/after-files.sha256"
echo "-- starting checkout file diff (before vs after):"; diff "$F/before-files.sha256" "$F/after-files.sha256" && echo "identical"
(cd "$F/installed" && find . -type f -print0 | sort -z | xargs -0 shasum -a 256) > "$F/after-installed.sha256"
echo "-- installed diff:"; if cmp -s "$F/before-installed.sha256" "$F/after-installed.sha256"; then echo identical; else diff "$F/before-installed.sha256" "$F/after-installed.sha256" | grep "^[<>]" | sed "s/ [0-9a-f]* / /"; fi
if [ -e "$F/repo/.git" ]; then
  { git -C "$F/repo" branch --show-current; git -C "$F/repo" rev-parse HEAD; git -C "$F/repo" status --porcelain; } > "$F/after-git-start.txt"
  echo "-- starting branch/HEAD/status diff:"; diff <(head -n $(wc -l < "$F/after-git-start.txt") "$F/before-git.txt") "$F/after-git-start.txt" && echo "identical"
  echo "-- worktrees:"; git -C "$F/repo" worktree list --porcelain
  echo "-- branches:"; git -C "$F/repo" branch -vv --list
  for b in $(git -C "$F/repo" for-each-ref --format='%(refname:short)' refs/heads); do
    [ "$b" = main ] || [ "$b" = feat/unrelated-work ] && continue
    echo "-- $b vs main:"; git -C "$F/repo" log --oneline main..$b; git -C "$F/repo" diff --stat main...$b
    echo "-- merge-base == main? $( [ "$(git -C "$F/repo" merge-base main $b)" = "$(git -C "$F/repo" rev-parse main)" ] && echo yes || echo no )"
  done
  for w in $(git -C "$F/repo" worktree list --porcelain | awk '/^worktree /{print $2}'); do
    [ "$w" -ef "$F/repo" ] && continue; echo "-- status in $w:"; git -C "$w" status --short --branch
  done
fi
echo "-- other new paths under fixture:"; find "$F" -maxdepth 2 -mindepth 1 -not -name '*.sha256' -not -name '*.txt' -not -path "$F/repo*" -not -path "$F/installed*"
