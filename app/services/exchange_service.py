import httpx

RATE_CACHE = {}

NBP_API_URL = "https://api.nbp.pl/api/exchangerates/rates/c/"

async def get_exchange_rate(currency: str) -> float:
    currency = currency.upper()

    if currency in RATE_CACHE:
        return RATE_CACHE[currency]

    url = f"{NBP_API_URL}{currency}/?format=json"
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.get(url)

    if response.status_code == 200:
        data = response.json()
        try:
            ask_price = data["rates"][0]["ask"]
            RATE_CACHE[currency] = ask_price
            return ask_price
        except (KeyError, IndexError):
            print(f"Unexpected data format from NBP for {currency}: {data}")
            return 0.0
    else:
        print(f"NBP API returned status {response.status_code} for {currency}")
        return 0.0