def model_spend(balance, amount):
    return balance - amount if amount <= balance else balance
for balance in range(3):
    for amount in range(4):
        assert model_spend(balance, amount) >= 0
print('bounded model passed: balances 0..2, amounts 0..3')
