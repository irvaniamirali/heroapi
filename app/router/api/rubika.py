from fastapi import APIRouter, Response, status

from typing import Optional

from bs4 import BeautifulSoup

import html_to_json
import langdetect
import json

from httpx import AsyncClient, codes

client = AsyncClient()

router = APIRouter()


@router.get("/rubika-info", tags=["Icon Search"], status_code=status.HTTP_200_OK)
@router.post("/rubika-info", tags=["Icon Search"], status_code=status.HTTP_200_OK)
async def rubika_info(response: Response, query: str) -> dict:
    """
    Web Service to get rubika users information
    """
    result = dict()
    request = await client.request(
        method="GET", url=f"https://rubika.ir/{query}"
    )
    if request.status_code != codes.OK:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "data": None,
            "error_message": "A problem has occurred on our end"
        }
    bs4 = BeautifulSoup(request.text, "html.parser")
    if bs4.head.title.text == "Rubika":
        result["profile"] = bs4.find("img", {"class":"dialog-avatar"}).attrs["src"]
        result["title"] = bs4.find("div", {"class":"l-title"}).text
        try:
            result["description"] = bs4.find("div", {"class":"l-desc"}).text
        except:
            result["description"] = None
        result["member_count"] = int(bs4.find("span", {"class":"user-last-message"}).text.replace(" مشترک ", ""))
        return {
            "success": True,
            "data": result,
            "error_message": None
        }
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "success": False,
            "data": result,
            "error_message": "id not found."
        }
