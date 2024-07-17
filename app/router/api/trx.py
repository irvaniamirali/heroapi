from fastapi import APIRouter, Response, status

from bs4 import BeautifulSoup

import httpx

client = httpx.AsyncClient()

router = APIRouter(tags=["Crypto"])


@router.get("/tron", status_code=status.HTTP_200_OK)
@router.post("/tron", status_code=status.HTTP_200_OK)
async def tron(response: Response) -> dict:
    """
    In this api, by using request and crypto site, we get the current price of Tron currency...
    """
    request = await client.request(method="POST", url="https://arzdigital.com/coins/tron/")
    if request.status_code != httpx.codes.OK:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "data": None,
            "error_message": "A problem has occurred on our end"
        }

    soup = BeautifulSoup(request.content, "html.parser")
    price = soup.find(
        "div", {
            "class": "arz-coin-page-data__coin-toman-price"
        }
    )
    return {
        "success": True,
        "data": price.text.strip(),
        "error_message": None
    }
