wallet_data = {}

def add_currency(currency: str, amount: float):
    currency = currency.upper()
    if currency in wallet_data:
        wallet_data[currency] += amount
    else:
        wallet_data[currency] = amount

def subtract_currency(currency: str, amount: float):
    currency = currency.upper()
    if currency not in wallet_data:
        return
    wallet_data[currency] = max(wallet_data[currency] - amount, 0)

def get_wallet_contents():
    return wallet_data
