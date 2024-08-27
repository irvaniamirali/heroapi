from fastapi import APIRouter, Response, status

from typing import Optional

from bs4 import BeautifulSoup

import html_to_json
import langdetect

from httpx import AsyncClient, codes

client = AsyncClient()

router = APIRouter()


@router.get("/icon", tags=["Icon Search"], status_code=status.HTTP_200_OK)
@router.post("/icon", tags=["Icon Search"], status_code=status.HTTP_200_OK)
async def icon_search(response: Response, query: str, page: Optional[int] = 1) -> dict:
    """
    Web Service to search icon from [icon-icons](https://icon-icons.com)
    """
    request = await client.request(
        method="GET", url=f"https://icon-icons.com/search/icons/?filtro={query}&page={page}"
    )
    if request.status_code != codes.OK:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "data": None,
            "error_message": "A problem has occurred on our end"
        }

    soup = BeautifulSoup(request.text, "html.parser")
    icons = soup.find_all("div", class_="icon-preview")

    search_result = list()
    for icon in icons:
        data_original = icon.find("img", loading="lazy", src=True)
        search_result.append(data_original.get("src"))

    return {
        "success": True,
        "data": search_result,
        "error_message": None
    }


@router.get("/lang", tags=["Language Detect"], status_code=status.HTTP_200_OK)
@router.post("/lang", tags=["Language Detect"], status_code=status.HTTP_200_OK)
async def language_detect(response: Response, text: str) -> dict:
    """
    Identifying the language of texts
    """
    try:
        result_detected = langdetect.detect(text)
        return {
            "success": True,
            "data": result_detected,
            "error_message": None
        }
    except langdetect.LangDetectException:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "success": False,
            "data": None,
            "error_message": "The value of the `text` parameter is not invalid"
        }


@router.get("/html2json", tags=["Convert HTML to JSON"], status_code=status.HTTP_200_OK)
@router.post("/html2json", tags=["Convert HTML to JSON"], status_code=status.HTTP_200_OK)
async def convert_html_to_json(html: str) -> dict:
    """
    Convert HTML document to json
    """
    output_json = html_to_json.convert(html)
    return {
        "success": True,
        "data": output_json,
        "error_message": None
    }
