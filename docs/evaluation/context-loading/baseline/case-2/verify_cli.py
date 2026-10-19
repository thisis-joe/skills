"""Exercise all mapped public CLI features and retain process evidence."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence" / "cli"
CASES = [
    ("help-long", ["--help"], 0, None, ["--double", "--triple", "usage:"], []),
    ("help-short", ["-h"], 0, None, ["--double", "--triple", "usage:"], []),
    ("double-positive", ["--double", "3"], 0, "6\n", [], []),
    ("double-negative", ["--double", "-4"], 0, "-8\n", [], []),
    ("double-zero", ["--double", "0"], 0, "0\n", [], []),
    ("triple-positive", ["--triple", "3"], 0, "9\n", [], []),
    ("triple-negative", ["--triple", "-4"], 0, "-12\n", [], []),
    ("triple-zero", ["--triple", "0"], 0, "0\n", [], []),
    ("required-mode", [], 2, "", [], ["required"]),
    ("exclusive-modes", ["--double", "3", "--triple", "3"], 2, "", [], ["not allowed with argument"]),
    ("double-invalid-integer", ["--double", "x"], 2, "", [], ["invalid int value"]),
    ("triple-invalid-integer", ["--triple", "x"], 2, "", [], ["invalid int value"]),
    ("double-missing-value", ["--double"], 2, "", [], ["expected one argument"]),
    ("triple-missing-value", ["--triple"], 2, "", [], ["expected one argument"]),
    ("unknown-option", ["--double", "3", "--unknown"], 2, "", [], ["unrecognized arguments"]),
]

def main():
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    records = []
    for name, args, exit_code, stdout, stdout_parts, stderr_parts in CASES:
        command = [sys.executable, "app.py", *args]
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        checks = {
            "exit": result.returncode == exit_code,
            "stdout": stdout is None or result.stdout == stdout,
            "stdout_fragments": all(p in result.stdout for p in stdout_parts),
            "stderr_fragments": all(p in result.stderr for p in stderr_parts),
            "success_stderr_empty": exit_code != 0 or result.stderr == "",
        }
        for suffix, value in [("stdout", result.stdout), ("stderr", result.stderr),
                              ("exit", str(result.returncode) + "\n")]:
            (EVIDENCE / (name + "." + suffix + ".txt")).write_text(value)
        records.append({"feature": name, "command": command, "exit": result.returncode,
                        "stdout": result.stdout, "stderr": result.stderr,
                        "expected_exit": exit_code, "expected_stdout": stdout,
                        "checks": checks, "status": "passed" if all(checks.values()) else "failed",
                        "evidence": ["evidence/cli/" + name + "." + x + ".txt"
                                     for x in ["stdout", "stderr", "exit"]]})
        print(name + ": " + records[-1]["status"])
    report = {"snapshot": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                            for name in ["app.py", "test_app.py"]},
              "python": sys.version, "checks": records,
              "cleanup": "All child processes completed; no server or fixture state was created.",
              "evidence_exists": all((ROOT / path).is_file() for record in records for path in record["evidence"])}
    (EVIDENCE / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    return 0 if report["evidence_exists"] and all(r["status"] == "passed" for r in records) else 1

if __name__ == "__main__":
    raise SystemExit(main())
