from fastapi import APIRouter, Depends
from app.services import wallet_service, exchange_service
from app.schemas.wallet import WalletOverview, CurrencyValue
from app.core.security import verify_api_key

router = APIRouter()

@router.get("/", response_model=WalletOverview)
async def get_wallet():
    wallet = wallet_service.get_wallet_contents()
    return await _build_wallet_overview(wallet)

@router.post("/add/{currency}/{amount}", response_model=WalletOverview, dependencies=[Depends(verify_api_key)])
async def add_to_wallet(currency: str, amount: float):
    wallet_service.add_currency(currency, amount)

    wallet = wallet_service.get_wallet_contents()
    return await _build_wallet_overview(wallet)

@router.post("/sub/{currency}/{amount}", response_model=WalletOverview, dependencies=[Depends(verify_api_key)])
async def subtract_from_wallet(currency: str, amount: float):
    wallet_service.subtract_currency(currency, amount)

    wallet = wallet_service.get_wallet_contents()
    return await _build_wallet_overview(wallet)

async def _build_wallet_overview(wallet_data: dict) -> WalletOverview:
    """Helper function to build WalletOverview from raw wallet data."""
    currencies = {}
    total_pln = 0.0
    for currency, amount in wallet_data.items():
        rate = await exchange_service.get_exchange_rate(currency)
        pln_value = amount * rate
        currencies[currency] = CurrencyValue(amount=amount, pln_value=pln_value)
        total_pln += pln_value
    return WalletOverview(currencies=currencies, total_pln=total_pln)