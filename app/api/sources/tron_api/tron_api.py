from httpx import AsyncClient

from bs4 import BeautifulSoup

client = AsyncClient()


async def tron():
    response = await client.request("POST", url="https://arzdigital.com/coins/tron/")
    soup = BeautifulSoup(response.content, "html.parser")
    price = soup.find(
        "div", {
            "class": "arz-coin-page-data__coin-toman-price"
        }
    )
    return {"output": price.text.strip()}
