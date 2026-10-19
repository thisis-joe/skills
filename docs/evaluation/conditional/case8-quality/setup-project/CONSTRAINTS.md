# Standing quality bar — local preparation v1
Owner: project maintainer; setup owner lets-start. Execution/fixes/real project commit belong to lets-build. Canonical policy is this file, linked by project README. No prior bar exists. Branch feature/setup-project, base ab430b26788f0f48a73382dd400c7ced99b04f49; initial fixture was clean. Project is Python stdlib CLI, documented syntax/unittest commands match CI; task state stays TASKS.md.

| Rule/reason | Exact checker | Scope/stage | Disposition |
|---|---|---|---|
| Preserve floor: lower thresholds, weaker/deleted assertions/tests, new skips/suppressions/exceptions require review | python3 /tmp/lets-conditional-validation/case8-quality/floor_guard.py --repo . --base fixture/main | complete committed/staged/unstaged/untracked task scope; task closure and proposed CI | Exit 0 clean, 1 heuristic violation needs review, 2 unavailable blocks claim. Prototype detects a subset; manual floor inspection remains required. |
| Valid Python syntax | python3 -m py_compile src/report.py | changed source during edit/task closure | blocking on failure |
| Public CLI behavior remains correct | python3 -m unittest discover -s tests -v | task closure/CI | blocking on failure |
| Coverage observation | read artifacts/coverage.json, percent 82.5, line coverage, prior fixture measurement, full-suite Python CLI conditions | review/CI evidence reuse | measured-only; no target/noise tolerance set by user. No invented ratchet or rerun just for metrics. |

Unattended setup uses the floor and flags unset policy, no interview. Coverage target/ratchet and edit-loop latency budget remain maintainer decisions before enforcing those optional dimensions. No exception currently exists for this setup. Future exception must name rule/path/reason/owner/tracking/review date and have actual authorization. No web UI exists, so browser performance/accessibility dimensions are not applicable. Independent external quality scanner unavailable; self-authored heuristic is not that independent assessment. No checkers/dependencies/hooks/CI schedule are installed or activated by this draft.
