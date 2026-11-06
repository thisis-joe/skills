#!/usr/bin/env python3
"""Check case files and their entries in the TIL index."""
import argparse
from collections import Counter
from pathlib import Path
import sys

# Keep the managed skill directory free of cache files when running this CLI.
sys.dont_write_bytecode = True
from check_notes import (CheckError, SCHEME, SLUG, check_frontmatter, headings,
                         rendered_links, split_note)

CASE_KEYS = ('title', 'created', 'updated', 'sources')
CASE_SECTION = '문제 해결 사례'
TEMPLATE_NAME = 'CASE_TEMPLATE.md'


def inside_root(root, path):
    if not path.resolve().is_relative_to(root):
        raise CheckError(f'{path}: path escapes the TIL root')
    return path


def check_case(path, sections):
    problems = []

    def problem(line, message):
        problems.append(f'{path}:{line}: {message}')

    front, body, start = split_note(path.read_text(encoding='utf-8'))
    if front is None:
        problem(1, 'missing case frontmatter between --- lines')
        return problems
    fields = check_frontmatter(front, problem, CASE_KEYS)
    sources = fields.get('sources', '')
    if sources.startswith('[') and sources.endswith(']'):
        pointers = [item.strip() for item in sources[1:-1].split(',')]
        if any(not item or (item.startswith('<') and item.endswith('>')) for item in pointers):
            problem(1, 'sources must list actual evidence pointers')

    marks = headings(body)
    titles = [(line, name) for line, level, name in marks if level == 1]
    first = next((line for line, value in enumerate(body) if value.strip()), None)
    if len(titles) != 1 or titles[0] != (first, fields.get('title')):
        problem(start, 'start the case body with one level-one heading matching title')

    parts = [(line, name) for line, level, name in marks if level == 2]
    if [name for _, name in parts] != sections:
        problem(start, 'case sections must be exactly, in order: ' + ' / '.join(sections))
    else:
        ends = [line for line, _ in parts[1:]] + [len(body)]
        for (line, name), end in zip(parts, ends):
            if not any(value.strip() for value in body[line + 1:end]):
                problem(start + line, f'case section is empty: {name}')
    return problems


def check_index(root, targets):
    index = inside_root(root, root / 'INDEX.md')
    if not index.is_file():
        return [f'{index}:1: missing INDEX.md']
    lines = index.read_text(encoding='utf-8').splitlines()
    marks = [(line, level, name) for line, level, name in headings(lines) if level <= 2]
    sections = [line for line, level, name in marks if level == 2 and name == CASE_SECTION]
    if len(sections) != 1:
        return [f'{index}:1: expected exactly one level-two {CASE_SECTION} section']

    start = sections[0]
    end = next((line for line, _, _ in marks if line > start), len(lines))
    listed = Counter()
    problems = []
    case_paths = {path.resolve() for path in targets.values()}
    for line, target in rendered_links(lines):
        in_section = start < line < end
        relative = target.split('#', 1)[0]
        local_path = (root / relative) if relative and not SCHEME.match(target) else None
        case_link = local_path is not None and (
            relative.startswith('cases/') or local_path.resolve() in case_paths)
        if not (in_section or case_link):
            continue
        if target not in targets:
            problems.append(f'{index}:{line + 1}: expected a link to an existing cases/<slug>.md file: {target}')
        elif not in_section:
            problems.append(f'{index}:{line + 1}: list {target} only under {CASE_SECTION}')
        else:
            listed[target] += 1
    for target in targets:
        if listed[target] != 1:
            problems.append(f'{index}:{start + 1}: {target} is listed {listed[target]} times '
                            f'under {CASE_SECTION}, expected once')
    return problems


def check_workspace(root):
    root = root.resolve()
    template = inside_root(root, root / TEMPLATE_NAME)
    if not template.is_file():
        raise CheckError(f'{template}: missing {TEMPLATE_NAME}')
    sections = [name for _, level, name in headings(template.read_text(encoding='utf-8').splitlines())
                if level == 2]
    if len(sections) != 4 or len(set(sections)) != 4:
        raise CheckError(f'{template}: case template needs four distinct level-two sections')

    folder = inside_root(root, root / 'cases')
    paths = sorted(folder.glob('*.md'))
    if not paths:
        raise CheckError(f'{folder}: no case files')
    problems = []
    targets = {}
    for path in paths:
        inside_root(root, path)
        if not path.is_file() or not SLUG.fullmatch(path.name):
            problems.append(f'{path}:1: expected a case file with a lowercase-hyphen slug')
            continue
        problems.extend(check_case(path, sections))
        targets[path.relative_to(root).as_posix()] = path
    return problems + check_index(root, targets), len(targets)


def main(argv=None):
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path, help='TIL workspace directory')
    args = parser.parse_args(argv)
    try:
        problems, count = check_workspace(args.root)
    except (CheckError, OSError, UnicodeError, RuntimeError) as exc:
        parser.exit(2, f'{exc}\n')
    if problems:
        print('\n'.join(problems))
        return 1
    print(f"OK: {count} troubleshooting {'case' if count == 1 else 'cases'}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
