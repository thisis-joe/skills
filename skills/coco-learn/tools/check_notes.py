#!/usr/bin/env python3
"""Check coco-learn notes against the workspace template, length budget and index."""
import argparse
from collections import Counter
from datetime import date
from pathlib import Path
import re
import sys

# references/note-template.md documents these limits; change both together.
MAX_BODY_LINES = 60
MAX_SUMMARY_CHARS = 200
MAX_ITEM_CHARS = 160
MAX_CODE_LINES = 15
KEYS = ('title', 'tags', 'status', 'created', 'updated', 'sources')
STATUSES = ('learning', 'understood', 'review')
# Template sections by position, so translated labels keep their limits.
SECTIONS = (('bullets', 2, 5), ('example', 1, 1), ('bullets', 1, 3),
            ('questions', 1, 3), ('links', 0, 5))
SLUG = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\.md')
HEADING = re.compile(r'(#{1,6})\s+(.+?)(?:\s+#+)?\s*')
BULLET = re.compile(r'[-*] (\S.*)')
QUESTION = re.compile(r'<details><summary>.+</summary>.+</details>')
LINK = re.compile(r'\[[^\]\n]+\]\(([^)\s]+)\)')
SCHEME = re.compile(r'[a-zA-Z][a-zA-Z0-9+.-]*:')
FENCE = re.compile(r'\s*(```|~~~)')


class CheckError(Exception):
    pass


def split_note(text):
    """Return frontmatter lines, body lines and the body's first line number."""
    lines = text.splitlines()
    if lines and lines[0] == '---':
        for index in range(1, len(lines)):
            if lines[index] == '---':
                return lines[1:index], lines[index + 1:], index + 2
    return None, lines, 1


def outside_fences(lines):
    """Yield (index, line, in_code) so headings inside code are not sections."""
    in_code = False
    for index, line in enumerate(lines):
        if FENCE.match(line):
            in_code = not in_code
            yield index, line, True
            continue
        yield index, line, in_code


def headings(lines):
    found = []
    for index, line, in_code in outside_fences(lines):
        match = None if in_code else HEADING.fullmatch(line)
        if match:
            found.append((index, len(match.group(1)), match.group(2)))
    return found


def template_sections(path):
    if not path.is_file():
        raise CheckError(f'{path}: missing TEMPLATE.md')
    _, body, _ = split_note(path.read_text(encoding='utf-8'))
    names = [text for _, level, text in headings(body) if level == 2]
    if len(names) != len(SECTIONS):
        raise CheckError(f'{path}: template needs exactly {len(SECTIONS)} level-two '
                         f'sections, found {len(names)}')
    return names


def check_frontmatter(front, problem):
    fields = {}
    for number, line in enumerate(front, 2):
        key, sep, value = line.partition(':')
        key = key.strip()
        if not sep or key not in KEYS or key in fields:
            problem(number, f'unexpected frontmatter line: {line.strip()}')
            continue
        fields[key] = value.strip()
    for key in KEYS:
        if key not in fields:
            problem(1, f'missing frontmatter key: {key}')
    if 'status' in fields and fields['status'] not in STATUSES:
        problem(1, 'status must be one of: ' + ', '.join(STATUSES))
    days = {}
    for key in ('created', 'updated'):
        if key in fields:
            try:
                days[key] = date.fromisoformat(fields[key])
            except ValueError:
                problem(1, f'{key} must be YYYY-MM-DD')
    if len(days) == 2 and days['updated'] < days['created']:
        problem(1, 'updated is earlier than created')
    for key in ('tags', 'sources'):
        value = fields.get(key)
        if value is not None and not (value.startswith('[') and value.endswith(']')):
            problem(1, f'{key} must be a [list]')
        elif key == 'tags' and value is not None and not value[1:-1].strip():
            problem(1, 'tags needs at least one topic')
    return fields


def check_section(kind, low, high, lines, first, problem):
    """Check one section's raw lines; first is the line number of lines[0]."""
    if kind == 'example':
        fences = code_lines = 0
        for _, line, in_code in outside_fences(lines):
            if FENCE.match(line):
                fences += 1
            elif in_code:
                code_lines += 1
        if not any(line.strip() for line in lines):
            problem(first, 'example is empty')
        if fences > 2:
            problem(first, 'example holds more than one code block')
        if code_lines > MAX_CODE_LINES:
            problem(first, f'example code has {code_lines} lines; limit is {MAX_CODE_LINES}')
        return
    items = 0
    for offset, line in enumerate(lines):
        if not line.strip():
            continue
        number = first + offset
        if kind == 'questions':
            if not QUESTION.fullmatch(line.strip()):
                problem(number, 'write each question as one '
                                '<details><summary>question</summary>answer</details> line')
                continue
            items += 1
            continue
        match = BULLET.fullmatch(line)
        if not match:
            problem(number, 'use one top-level bullet per line')
            continue
        items += 1
        if kind == 'links' and not LINK.search(line):
            problem(number, 'related bullet needs a link')
        if kind == 'bullets' and len(match.group(1)) > MAX_ITEM_CHARS:
            problem(number, f'bullet has {len(match.group(1))} characters; '
                            f'limit is {MAX_ITEM_CHARS}')
    if not low <= items <= high:
        noun = 'questions' if kind == 'questions' else 'bullets'
        problem(first - 1, f'section has {items} {noun}; expected {low}-{high}')


def check_note(path, sections):
    """Return (problems, frontmatter fields) for one note."""
    problems = []

    def problem(line, message):
        problems.append(f'{path}:{line}: {message}')

    front, body, start = split_note(path.read_text(encoding='utf-8'))
    if front is None:
        problem(1, 'missing frontmatter between --- lines')
        return problems, {}
    fields = check_frontmatter(front, problem)
    while body and not body[-1].strip():
        body.pop()
    if len(body) > MAX_BODY_LINES:
        problem(start, f'{len(body)} lines after frontmatter; limit is {MAX_BODY_LINES}. '
                       'Split the note by concept')
    marks = headings(body)
    titles = [mark for mark in marks if mark[1] == 1]
    parts = [mark for mark in marks if mark[1] == 2]
    allowed = {index for index, _, _ in titles[:1] + parts}
    for index, _, _ in marks:
        if index not in allowed:
            problem(start + index, 'only the title and the template sections may be headings')
    content = [index for index, line in enumerate(body) if line.strip()]
    if len(titles) != 1 or not content or content[0] != titles[0][0]:
        problem(start, 'start the body with exactly one level-one title')
    elif titles[0][2] != fields.get('title'):
        problem(start + titles[0][0], 'title heading differs from frontmatter title')
    if titles:
        end = parts[0][0] if parts else len(body)
        summary = [index for index in range(titles[0][0] + 1, end) if body[index].strip()]
        if len(summary) != 1 or not body[summary[0]].startswith('> '):
            problem(start + titles[0][0] + 1, 'put exactly one "> summary" line under the title')
        elif len(body[summary[0]]) - 2 > MAX_SUMMARY_CHARS:
            problem(start + summary[0], f'summary is longer than {MAX_SUMMARY_CHARS} characters')
    names = [name for _, _, name in parts]
    if names != list(sections):
        problem(start + (parts[0][0] if parts else 0),
                'sections must be exactly, in order: ' + ' / '.join(sections))
    else:
        ends = [index for index, _, _ in parts[1:]] + [len(body)]
        for (index, _, _), (kind, low, high), end in zip(parts, SECTIONS, ends):
            check_section(kind, low, high, body[index + 1:end], start + index + 1, problem)
    for offset, line in enumerate(body):
        for target in LINK.findall(line):
            relative = target.split('#', 1)[0]
            if relative and not SCHEME.match(target) and not (path.parent / relative).exists():
                problem(start + offset, f'broken link: {target}')
    return problems, fields


def find_template(note):
    for folder in (note.parent, note.parent.parent):
        if (folder / 'TEMPLATE.md').is_file():
            return folder / 'TEMPLATE.md'
    raise CheckError(f'{note}: no TEMPLATE.md beside the note or its folder; pass --template')


def check_workspace(root):
    """Return (problems, notes with fields) for INDEX.md, TEMPLATE.md and notes/."""
    sections = template_sections(root / 'TEMPLATE.md')
    folder = root / 'notes'
    notes = sorted(folder.glob('*.md')) if folder.is_dir() else []
    problems, checked, titles = [], [], {}
    for note in notes:
        if not SLUG.fullmatch(note.name):
            problems.append(f'{note}:1: name the file with a lowercase-hyphen slug')
        found, fields = check_note(note, sections)
        problems.extend(found)
        checked.append((note, fields))
        if fields.get('title'):
            titles.setdefault(fields['title'].casefold(), []).append(note)
    for paths in titles.values():
        for duplicate in paths[1:]:
            problems.append(f'{duplicate}:1: same title as {paths[0].name}; '
                            'keep one note per concept')
    index = root / 'INDEX.md'
    if not index.is_file():
        problems.append(f'{index}:1: missing INDEX.md')
        return problems, checked
    listed = Counter()
    for number, line in enumerate(index.read_text(encoding='utf-8').splitlines(), 1):
        for target in LINK.findall(line):
            relative = target.split('#', 1)[0]
            if SCHEME.match(target) or not relative:
                continue
            resolved = (root / relative).resolve()
            if not resolved.exists():
                problems.append(f'{index}:{number}: broken link: {target}')
            listed[resolved] += 1
    for note in notes:
        count = listed[note.resolve()]
        if count != 1:
            problems.append(f'{index}:1: {note.relative_to(root)} is listed {count} times; '
                            'list every note exactly once')
    return problems, checked


def summary(checked):
    statuses = Counter(fields.get('status') for _, fields in checked)
    counts = ', '.join(f'{status} {statuses[status]}' for status in STATUSES)
    noun = 'note' if len(checked) == 1 else 'notes'
    lines = [f'OK: {len(checked)} {noun} ({counts})']
    pending = sorted((fields.get('status') != 'review', fields.get('updated', ''), str(note))
                     for note, fields in checked
                     if fields.get('status') in ('review', 'learning'))
    if pending:
        lines.append('Reread next: ' + ', '.join(Path(item[2]).name for item in pending[:5]))
    return lines


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', type=Path, help='workspace directory or one note file')
    parser.add_argument('--template', type=Path,
                        help='TEMPLATE.md for a note outside a workspace')
    args = parser.parse_args(argv)
    try:
        if args.path.is_dir():
            problems, checked = check_workspace(args.path)
        elif args.path.is_file():
            template = args.template or find_template(args.path)
            problems, fields = check_note(args.path, template_sections(template))
            checked = [(args.path, fields)]
        else:
            raise CheckError(f'{args.path}: no such workspace or note')
    except CheckError as exc:
        parser.exit(2, f'{exc}\n')
    if problems:
        print('\n'.join(problems))
        return 1
    print('\n'.join(summary(checked)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
