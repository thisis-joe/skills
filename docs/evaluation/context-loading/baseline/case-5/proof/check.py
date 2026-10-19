"""Exhaustively check the current one-step spend model over unchanged bounds."""
import json


def model_spend(balance, amount):
    # wallet.spend is one unconditional subtraction, with no rejection branch.
    return balance - amount


def main():
    counterexamples = []
    checked = 0
    for balance in range(3):
        for amount in range(4):
            after = model_spend(balance, amount)
            checked += 1
            if after < 0:
                counterexamples.append({"balance": balance, "amount": amount,
                                        "model_after": after})
    report = {"property": "balance stays nonnegative after spend",
              "bounds": {"initial_balance": [0, 2], "amount": [0, 3], "steps": 1},
              "cases_checked": checked,
              "model_transition": "balance - amount (unconditional)",
              "property_holds": not counterexamples,
              "counterexamples": counterexamples}
    print(json.dumps(report, indent=2))
    return 1 if counterexamples else 0


if __name__ == "__main__":
    raise SystemExit(main())
