import os

API_KEY = os.environ.get("API_KEY")

if not API_KEY:
    raise ValueError("No API_KEY environment variable found. Please set it before running the application.")
