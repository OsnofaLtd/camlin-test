from pydantic import BaseSettings, Field
import logging

# Configure logging to display INFO level messages
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    """
    Application settings managed through environment variables.
    """
    api_key: str = Field(..., env="API_KEY", description="API key for authenticating requests.")

    class Config:
        """
        Configuration for Pydantic BaseSettings.
        """
        env_file = ".env"  # Specifies the file to read environment variables from
        env_file_encoding = 'utf-8'

settings = Settings()

logger.info("Configuration loaded successfully.")
