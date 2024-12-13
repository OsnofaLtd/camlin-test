from fastapi import FastAPI
from app.api.routes_wallet import router as wallet_router

app = FastAPI(title="Currency Wallet API", version="1.0.0")

app.include_router(wallet_router, prefix="/wallet", tags=["wallet"])

@app.get("/")
async def root():
  return {"message": "Hello, world! This is your currency wallet API."}