---
title: Atomic replace with os.replace
tags: [python, filesystem]
status: understood
created: 2026-10-20
updated: 2026-10-20
sources: [https://docs.python.org/3/library/os.html#os.replace]
---

# Atomic replace with os.replace

> `os.replace(src, dst)` moves a finished file over the target in one step, so readers see the old or the new file, never half of one.

## Key points

- Write the new content to a temporary path first, then `os.replace` it over the target.
- On POSIX the rename is atomic when both paths are on the same filesystem.
- It silently replaces an existing file, unlike `os.rename` on Windows, which raises.
- Create the temporary file next to the target so both share a filesystem.

## Example

```python
tmp = target.with_name(target.name + '.tmp')
tmp.write_text(content)
os.replace(tmp, target)  # readers never see a partial file
```

## Pitfalls

- Atomic is not durable: `fsync` the file and its directory if a crash must not lose it.
- A temporary file under `/tmp` may sit on another filesystem, where the call raises `OSError`.

## Self-check

<details><summary>Why create the temporary file next to the target?</summary>The rename is atomic only within one filesystem; a sibling path guarantees that.</details>
<details><summary>What does os.replace not promise after a power loss?</summary>Durability: the data may still be cached until it is synced.</details>

## Related

- [Python documentation: os.replace](https://docs.python.org/3/library/os.html#os.replace)
