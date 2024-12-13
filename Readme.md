# Currency Wallet API

A RESTful API to track the value of a user's wallet containing various foreign currencies and calculate their total worth in Polish złoty (PLN).

## Features

- **Wallet Management**: Add or remove amounts of various foreign currencies.
- **Real-Time Currency Conversion**: Fetch current exchange rates from the Polish National Bank (NBP) public API.
- **PLN Value Calculation**: Get the PLN equivalent of each currency held, as well as the total PLN value of the entire wallet.

## Endpoints

- `GET /wallet`: Returns the current wallet composition, each currency's PLN value, and the total PLN value.
- `POST /wallet/add/{currency}/{amount}`: Adds the specified amount of the given currency to the wallet. *(Protected)*
- `POST /wallet/sub/{currency}/{amount}`: Subtracts the specified amount of the given currency from the wallet. *(Protected)*

### Example Response for `GET /wallet`:

```json
{
  "currencies": {
    "EUR": {"amount": 100, "pln_value": 425},
    "USD": {"amount": 20, "pln_value": 77},
    "JPY": {"amount": 8000, "pln_value": 216}
  },
  "total_pln": 718
}
```
## Getting Started

### Prerequisites

- **Docker** installed on your machine.

### Environment Variables

Copy the `.env.example` file in the project root to `.env` to setup the API_KEY

## Build and Run the Container

```bash
docker-compose up --build
```
This command builds the Docker image and starts the container, loading environment variables from the `.env` file.

Retrieving the wallet
--------------

### Public Endpoint

`curl http://localhost:8000/wallet`


Updating the wallet
===================
### Protected Endpoints (Require API Key)

Add Currency
------------

`curl -X POST http://localhost:8000/wallet/add/EUR/100 -H "X-API-KEY: your_secret_api_key"`

Subtract Currency
-----------------

`curl -X POST http://localhost:8000/wallet/sub/EUR/50\ -H "X-API-KEY: your_secret_api_key"`

Interactive Documentation
=========================

-   [OpenAPI Docs](http://localhost:8000/docs)
-   [ReDoc](http://localhost:8000/redoc)
