from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from app.core.config import API_KEY

API_KEY_HEADER = "X-API-KEY"

api_key_header = APIKeyHeader(name=API_KEY_HEADER, auto_error=True)

def verify_api_key(incoming_key: str = Security(api_key_header)):
    if incoming_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return True