from fastapi import APIRouter, Response, status

from bs4 import BeautifulSoup

import httpx

client = httpx.AsyncClient()

router = APIRouter(tags=["Dictionary"])


async def async_request(path):
    """
    Make asynchronous request
    """
    response = await client.request(method="GET", url=path)
    return response


@router.get("/dict/v1", status_code=status.HTTP_200_OK)
@router.post("/dict/v1", status_code=status.HTTP_200_OK)
async def dictionary_search_v1(response: Response, query: str) -> dict:
    """
    Search words in deh [khoda](https://dehkhoda.ut.ac.ir) dictionary
    """
    path = f"https://dehkhoda.ut.ac.ir/fa/dictionary/{query}"
    request = await async_request(path=path)
    if request.status_code != httpx.codes.OK:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "data": None,
            "error_message": "A problem has occurred on our end"
        }

    soup = BeautifulSoup(request.text, "html.parser")
    paragraphs = soup.find("div", class_="definitions p-t-1")

    if not paragraphs:
        return {
            "success": False,
            "data": None,
            "error": "Your word was not found in the dictionary"
        }

    return {
        "success": True,
        "data": paragraphs.text,
        "error_message": None
    }
