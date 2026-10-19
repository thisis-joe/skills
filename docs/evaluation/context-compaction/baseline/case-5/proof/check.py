"""Exhaustive one-step bounded check, grounded in the current wallet function.

Run from the case directory: python3 proof/check.py
Exit 0: all 12 bounded transitions correspond and preserve nonnegative balance.
Exit 1: a property violation or model/code mismatch was observed.
"""
import hashlib
import importlib.util
import json
from pathlib import Path

BALANCES = range(3)
AMOUNTS = range(4)
WALLET_PATH = Path(__file__).resolve().parents[1] / "wallet.py"


def model_spend(balance, amount):
    # wallet.spend performs one unconditional subtraction. There is no guard.
    return balance - amount


def main():
    spec = importlib.util.spec_from_file_location("bounded_wallet_target", WALLET_PATH)
    wallet = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(wallet)
    violations = []
    mismatches = []
    checked = 0
    for balance in BALANCES:
        for amount in AMOUNTS:
            checked += 1
            modeled = model_spend(balance, amount)
            actual = wallet.spend(balance, amount)
            transition = {"balance": balance, "amount": amount,
                          "model_result": modeled, "actual_result": actual}
            if actual != modeled:
                mismatches.append(transition)
            # Keep the original property and bounds; no overspending exclusion.
            if actual < 0 or modeled < 0:
                violations.append(transition)
    report = {
        "property": "balance stays nonnegative",
        "bounds": {"initial_balance": [0, 2], "amount": [0, 3], "steps": 1},
        "checked_transitions": checked,
        "wallet_sha256": hashlib.sha256(WALLET_PATH.read_bytes()).hexdigest(),
        "model_code_mismatches": mismatches,
        "property_violations": violations,
        "status": "failed" if violations or mismatches else "passed",
    }
    print(json.dumps(report, indent=2))
    return 1 if violations or mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
