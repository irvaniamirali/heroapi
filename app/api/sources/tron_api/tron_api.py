from fastapi import status

from httpx import AsyncClient, codes

from bs4 import BeautifulSoup

client = AsyncClient()


async def tron():
    """
    In this sources, by using request and crypto site, we get the current price of Tron currency...
    """
    response = await client.request("POST", url="https://arzdigital.com/coins/tron/")
    soup = BeautifulSoup(response.content, "html.parser")
    price = soup.find(
        "div", {
            "class": "arz-coin-page-data__coin-toman-price"
        }
    )
    return {"output": price.text.strip()}
