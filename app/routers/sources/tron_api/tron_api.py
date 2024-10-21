from fastapi import APIRouter, status

from app.api.sources.tron_api import tron as tron_api

router = APIRouter(prefix="/api", tags=["Tron"])


@router.post("/tron", status_code=status.HTTP_200_OK)
async def tron() -> dict:
    """
    In this api, by using request and crypto site, we get the current price of Tron currency...
    """
    return await tron_api()
