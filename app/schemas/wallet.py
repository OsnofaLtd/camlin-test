from pydantic import BaseModel
from typing import Dict

class CurrencyValue(BaseModel):
    amount: float
    pln_value: float

class WalletOverview(BaseModel):
    currencies: Dict[str, CurrencyValue]
    total_pln: float
