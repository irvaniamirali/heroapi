from fastapi import APIRouter, Response, status

from app.api.sources.tron_api import tron

router = APIRouter(prefix="/api", tags=["Tron"])


@router.get("/tron", status_code=status.HTTP_200_OK)
@router.post("/tron", status_code=status.HTTP_200_OK)
async def tron(response: Response) -> dict:
    """
    In this api, by using request and crypto site, we get the current price of Tron currency...
    """
    return await tron(response)
