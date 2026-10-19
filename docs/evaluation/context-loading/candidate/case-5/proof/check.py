"""Exhaustive one-call bounded check; 0 pass, 1 property bug, 2 model drift."""
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("checked_wallet", ROOT / "wallet.py")
wallet = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wallet)


def model_spend(balance, amount):
    # wallet.spend has one unconditional subtraction and no rejection branch.
    return balance - amount


def main():
    mismatches = []
    counterexamples = []
    checked = 0
    for balance in range(3):
        for amount in range(4):
            modeled = model_spend(balance, amount)
            actual = wallet.spend(balance, amount)
            checked += 1
            if actual != modeled:
                mismatches.append({"balance": balance, "amount": amount,
                                   "model": modeled, "actual": actual})
            if modeled < 0 or actual < 0:
                counterexamples.append({"balance": balance, "amount": amount,
                                        "model": modeled, "actual": actual})
    status = "model-drift" if mismatches else "bug" if counterexamples else "passed"
    print(json.dumps({
        "status": status,
        "property": "spend(balance, amount) >= 0",
        "bounds": {"initial_balance": [0, 2], "amount": [0, 3], "calls": 1},
        "checked": checked,
        "wallet_sha256": hashlib.sha256((ROOT / "wallet.py").read_bytes()).hexdigest(),
        "python": platform.python_version(),
        "model_code_mismatches": mismatches,
        "counterexamples": counterexamples,
    }, indent=2))
    return 2 if mismatches else 1 if counterexamples else 0


if __name__ == "__main__":
    raise SystemExit(main())
