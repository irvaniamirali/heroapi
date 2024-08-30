from fastapi import status

from httpx import AsyncClient, codes

from bs4 import BeautifulSoup

client = AsyncClient()


async def tron(response):
    """
    In this api, by using request and crypto site, we get the current price of Tron currency...
    """
    request = await client.request("POST", url="https://arzdigital.com/coins/tron/")
    if request.status_code != codes.OK:
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
