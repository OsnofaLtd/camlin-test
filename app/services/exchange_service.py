import httpx  # Importing httpx for making asynchronous HTTP requests
import time   # Importing time for handling timestamps
import logging  # Importing logging for error and info messages

RATE_CACHE = {}
CACHE_TTL = 600  # 10 minutes

# Base URL for the NBP (National Bank of Poland) API to fetch exchange rates
NBP_API_URL = "https://api.nbp.pl/api/exchangerates/rates/c/"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_exchange_rate(currency: str) -> float:
    """
    Retrieve the current exchange rate for a specified currency from the NBP API.
    Implements a cache with TTL to minimize API calls and ensure data freshness.

    Args:
        currency (str): The 3-letter currency code (e.g., 'USD', 'EUR').

    Returns:
        float: The ask price of the currency in PLN. Returns 0.0 if the rate cannot be retrieved.
    """
    currency = currency.upper()
    current_time = time.time()  # Get the current timestamp

    # Check if the exchange rate for the currency is already cached
    if currency in RATE_CACHE:
        cached_rate, timestamp = RATE_CACHE[currency]
        # Calculate the age of the cached rate
        age = current_time - timestamp
        if age < CACHE_TTL:
            logger.info(f"Using cached exchange rate for {currency}: {cached_rate} PLN")
            return cached_rate  # Return the cached rate if it's still valid
        else:
            logger.info(f"Cached exchange rate for {currency} expired. Fetching new rate.")
            del RATE_CACHE[currency]  # Remove expired cache entry

    url = f"{NBP_API_URL}{currency}/?format=json"

    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            response = await client.get(url)  # Make a GET request to the API
        except httpx.RequestError as e:
            # Handle request exceptions (e.g., network issues)
            logger.error(f"An error occurred while requesting {url}: {e}")
            return 0.0

    if response.status_code == 200:
        try:
            data = response.json()
            ask_price = data["rates"][0]["ask"]
            RATE_CACHE[currency] = (ask_price, current_time)
            logger.info(f"Fetched and cached exchange rate for {currency}: {ask_price} PLN")
            return ask_price
        except (KeyError, IndexError, ValueError) as e:
            logger.error(f"Unexpected data format from NBP for {currency}: {e}")
            return 0.0
    else:
        logger.error(f"NBP API returned status {response.status_code} for {currency}")
        return 0.0
