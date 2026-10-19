# Maintained COCO fixture

This is a synthetic, local package for one bounded application.

For this maintained package, run `python3 scripts/validate.py` and `python3 -m unittest discover -s tests -v`, as required by AGENTS.md and CI. See the shared contract for conditional check selection and caller-impact review.

Installation uses `python3 scripts/install.py --dest <explicit-local-folder>`. Do not infer a global destination.
