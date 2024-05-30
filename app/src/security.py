from fastapi import Header, HTTPException
from typing import Annotated
import os


api_secret_key = os.getenv("API_SECRET_KEY")
if not api_secret_key:
    raise ValueError("API_SECRET_KEY environment variable not set")

# Simple authentication logic to avoid bots
async def verify_api_key(api_key: Annotated[str, Header()]):
    # Verify API key
    if api_key != api_secret_key:
        raise HTTPException(status_code=400, detail="Api-Key header invalid")
