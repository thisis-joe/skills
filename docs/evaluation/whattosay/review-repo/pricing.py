def total(price, quantity, member=False):
    amount = price * quantity
    if member or quantity >= 3:
        return amount * 0.9
    return amount
