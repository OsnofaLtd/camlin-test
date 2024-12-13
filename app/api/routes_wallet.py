from fastapi import APIRouter, Depends
from app.services import wallet_service, exchange_service
from app.schemas.wallet import WalletOverview, CurrencyValue
from app.core.security import verify_api_key

router = APIRouter()

@router.get("/", response_model=WalletOverview)
async def get_wallet():
    """
    Retrieve the current contents of the wallet.

    Returns:
        WalletOverview: An overview of all currencies in the wallet and their total PLN value.
    """
    # Fetch the current wallet contents from the wallet_service
    wallet = wallet_service.get_wallet_contents()
    # Build and return the WalletOverview response
    return await _build_wallet_overview(wallet)

@router.post("/add/{currency}/{amount}", response_model=WalletOverview, dependencies=[Depends(verify_api_key)])
async def add_to_wallet(currency: str, amount: float):
    """
    Add a specified amount of a currency to the wallet.

    Args:
        currency (str): The currency code to add (e.g., 'USD', 'EUR').
        amount (float): The amount of the currency to add.

    Returns:
        WalletOverview: Updated overview of the wallet after addition.
    """
    # Add the specified currency and amount to the wallet
    wallet_service.add_currency(currency, amount)

    # Fetch the updated wallet contents
    wallet = wallet_service.get_wallet_contents()
    # Build and return the updated WalletOverview response
    return await _build_wallet_overview(wallet)

@router.post("/sub/{currency}/{amount}", response_model=WalletOverview, dependencies=[Depends(verify_api_key)])
async def subtract_from_wallet(currency: str, amount: float):
    """
    Subtract a specified amount of a currency from the wallet.

    Args:
        currency (str): The currency code to subtract (e.g., 'USD', 'EUR').
        amount (float): The amount of the currency to subtract.

    Returns:
        WalletOverview: Updated overview of the wallet after subtraction.
    """
    # Subtract the specified currency and amount from the wallet
    wallet_service.subtract_currency(currency, amount)

    # Fetch the updated wallet contents
    wallet = wallet_service.get_wallet_contents()
    # Build and return the updated WalletOverview response
    return await _build_wallet_overview(wallet)

async def _build_wallet_overview(wallet_data: dict) -> WalletOverview:
    """
    Helper function to build WalletOverview from raw wallet data.

    Args:
        wallet_data (dict): Dictionary containing currency codes and their respective amounts.

    Returns:
        WalletOverview: Structured overview of wallet contents with currency values and total PLN.
    """
    currencies = {}
    total_pln = 0.0
    # Iterate through each currency and amount in the wallet
    for currency, amount in wallet_data.items():
        # Retrieve the exchange rate for the currency
        rate = await exchange_service.get_exchange_rate(currency)
        # Calculate the PLN value of the currency
        pln_value = amount * rate
        # Create a CurrencyValue object and add it to the currencies dictionary
        currencies[currency] = CurrencyValue(amount=amount, pln_value=pln_value)
        # Accumulate the total PLN value
        total_pln += pln_value
    # Return the WalletOverview object containing all currencies and the total PLN value
    return WalletOverview(currencies=currencies, total_pln=total_pln)
