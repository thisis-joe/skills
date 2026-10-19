"""Replay every bounded model counterexample against the real public function."""
import importlib.util
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("wallet_under_verification", ROOT / "wallet.py")
wallet = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wallet)


def main():
    examples = json.loads((ROOT / "proof/counterexamples.json").read_text())
    results = []
    for example in examples:
        after = wallet.spend(example["balance"], example["amount"])
        results.append({**example, "actual_after": after,
                        "model_matches_code": after == example["model_after"],
                        "property_holds": after >= 0})
    positive = wallet.spend(2, 1)
    report = {"public_boundary": "wallet.spend(balance, amount)",
              "replays": results,
              "positive_observer": {"balance": 2, "amount": 1, "expected_after": 1,
                                    "actual_after": positive, "matches": positive == 1},
              "all_counterexamples_reproduced": bool(results) and all(
                  r["model_matches_code"] and not r["property_holds"] for r in results)}
    print(json.dumps(report, indent=2))
    if not report["all_counterexamples_reproduced"] or positive != 1:
        return 2  # Replay/model mismatch, not a confirmed counterexample.
    return 1  # The nonnegative property really fails.


if __name__ == "__main__":
    raise SystemExit(main())
