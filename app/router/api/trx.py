from fastapi import APIRouter, Response, status

from bs4 import BeautifulSoup

import httpx

client = httpx.AsyncClient()

router = APIRouter(prefix='/api', tags=["Crypto"])


@router.get("/tron", status_code=status.HTTP_200_OK)
@router.post("/tron", status_code=status.HTTP_200_OK)
async def tron(response: Response) -> dict:
    """
    In this api, by using request and crypto site, we get the current price of Tron currency...
    """
    req = await client.request(method="POST", url="https://arzdigital.com/coins/tron/")
    soup = BeautifulSoup(req.content, "html.parser")
    if req.status_code != httpx.codes.OK:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "error_message": "A problem has occurred on our end"
        }

    price = soup.find(
        "div", {
            "class": "arz-coin-page-data__coin-toman-price"
        }
    )
    return {
        "success": True,
        "data": {
            "price_tron": price.text.strip()
        }
    }
