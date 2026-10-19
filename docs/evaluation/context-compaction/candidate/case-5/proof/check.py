"""Finite bounded balance check aligned to current wallet.spend; see README.md."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("bounded_wallet", ROOT / "wallet.py")
wallet = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wallet)


def model_spend(balance, amount):
    # One pure, sequential call in wallet.py directly subtracts amount.
    return balance - amount


def main():
    correspondence = []
    counterexamples = []
    for balance in range(3):
        for amount in range(4):
            modeled = model_spend(balance, amount)
            actual = wallet.spend(balance, amount)
            record = {"balance": balance, "amount": amount,
                      "model_result": modeled, "actual_result": actual}
            if modeled != actual:
                correspondence.append(record)
            if modeled < 0 or actual < 0:
                counterexamples.append(record)
    result = {
        "property": "balance stays nonnegative after spend",
        "wallet_sha256": hashlib.sha256((ROOT / "wallet.py").read_bytes()).hexdigest(),
        "bounds": {"balance": [0, 2], "amount": [0, 3], "steps": 1},
        "checked_input_pairs": 12,
        "model_code_mismatches": correspondence,
        "counterexamples": counterexamples,
        "status": "failed" if correspondence or counterexamples else "passed",
    }
    print(json.dumps(result, indent=2))
    return 1 if correspondence or counterexamples else 0


if __name__ == "__main__":
    raise SystemExit(main())
