from typing import Dict

wallet_data: Dict[str, float] = {}

def add_currency(currency: str, amount: float) -> None:
    """
    Add a specified amount of a currency to the wallet.

    Args:
        currency (str): The 3-letter currency code to add (e.g., 'USD', 'EUR').
        amount (float): The amount of the currency to add.

    Raises:
        ValueError: If the amount is negative.
    """
    currency = currency.upper()

    if amount < 0:
        raise ValueError("Amount to add cannot be negative.")

    if currency in wallet_data:
        wallet_data[currency] += amount
    else:
        wallet_data[currency] = amount

def subtract_currency(currency: str, amount: float) -> None:
    """
    Subtract a specified amount of a currency from the wallet.

    Args:
        currency (str): The 3-letter currency code to subtract (e.g., 'USD', 'EUR').
        amount (float): The amount of the currency to subtract.

    Raises:
        ValueError:
            - If the amount is negative.
            - If the currency does not exist in the wallet.
            - If the subtraction results in a negative amount.
    """
    currency = currency.upper()

    if amount < 0:
        raise ValueError("Amount to subtract cannot be negative.")

    if currency not in wallet_data:
        raise ValueError(f"Currency '{currency}' not found in the wallet.")

    if wallet_data[currency] < amount:
        raise ValueError(f"Insufficient amount of '{currency}' to subtract {amount}.")

    wallet_data[currency] -= amount

    if wallet_data[currency] == 0:
        del wallet_data[currency]

def get_wallet_contents() -> Dict[str, float]:
    """
    Retrieve the current contents of the wallet.

    Returns:
        Dict[str, float]: A dictionary containing currency codes as keys and their respective amounts as values.
    """
    return wallet_data.copy()
