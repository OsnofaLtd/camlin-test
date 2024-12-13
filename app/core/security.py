from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from app.core.config import settings
import logging

# Configure logger for security module
logger = logging.getLogger(__name__)

# Define the header name for the API key
API_KEY_HEADER = "X-API-KEY"

# Initialize the APIKeyHeader with auto_error enabled to automatically handle missing headers
api_key_header = APIKeyHeader(name=API_KEY_HEADER, auto_error=True)

def verify_api_key(incoming_key: str = Security(api_key_header)) -> bool:
    """
    Verify the incoming API key against the predefined API key.

    Args:
        incoming_key (str): The API key extracted from the request header.

    Returns:
        bool: Returns True if the API key is valid.

    Raises:
        HTTPException: Raises a 401 Unauthorized error if the API key is invalid or missing.
    """
    if incoming_key != settings.api_key:
        logger.warning(f"Unauthorized access attempt with API key: {incoming_key}")
        # Raise an unauthorized error if the API key does not match
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    logger.info("API key verified successfully.")
    return True  # API key is valid
