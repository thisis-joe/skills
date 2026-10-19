# T1 result

Added --excited to the real Python CLI in the isolated fixture and committed only greet.py and tests/test_greet.py on feature/build. The new CLI path prints “Hello, Ada!”; normal output remains “Hello, Ada.”.

Behavioral red: new subprocess test failed because --excited was not recognized (exit 2 from CLI; suite exit 1). Minimal implementation added argparse's boolean flag and selected terminal punctuation. Green: both tests passed; both actual CLI invocations passed. Required regression suite is the same two-test stdlib suite. No deadline-based weakening occurred.

Scoped self-review covered the actual two unstaged task paths at snapshot recorded in evidence/review-scope.json, with independent spec/standards/quality verdicts in review.md. Independence is degraded and explicitly permitted by fixture rules; no independent model/agent review is claimed.

Commit and final authoritative state are in task-state.json and evidence/closure.json. Closure proves exactly two committed paths and unchanged SHA-256 for the pre-existing dirty NOTES.md. It remains dirty, unstaged, intact. State updates are external to the fixture repository by its documented convention, avoiding a circular commit-ID edit. No external publication, merge or deployment occurred. T1 is the only requested task; no next task was invented.
