"""Validate source traceability, skill format and installed references."""
import argparse
from pathlib import Path
from package_utils import PackageError, validate_package, validate_installed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--installed', type=Path)
    args = parser.parse_args()
    try:
        if args.installed:
            info = validate_installed(args.installed)
            print('Validated installed bundle: %d skills, %d files' %
                  (len(info['package']['skills']), len(info['files'])))
        else:
            data = validate_package(args.root)
            print('Validated package: %d skills, source checksums, coverage and references' % len(data['skills']))
    except (PackageError, KeyError, TypeError, OSError, ValueError) as exc:
        parser.exit(2, str(exc) + '\n')


if __name__ == '__main__':
    main()
