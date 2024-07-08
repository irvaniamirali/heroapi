from fastapi import APIRouter, Response, status

from typing import Optional

from bs4 import BeautifulSoup

import httpx
import re

client = httpx.AsyncClient()

router = APIRouter(prefix="/api", tags=["Music Search"])


@router.get("/music-fa", status_code=status.HTTP_200_OK)
@router.post("/music-fa", status_code=status.HTTP_200_OK)
async def music_fa(response: Response, query: str, page: Optional[int] = 1) -> dict:
    """
    Search and search web service on the [music-fa](https://music-fa.com) site
    """
    req = await client.request("GET", f"https://music-fa.com/search/{query}/page/{page}")
    if req.status_code != httpx.codes.OK:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "error_message": "A problem has occurred on our end"
        }

    soup = BeautifulSoup(req.text, "html.parser")
    articles = soup.find_all("article", class_="mf_pst")

    search_result = list()
    for article in articles:
        title = article["data-artist"].strip()
        image_snippet = article.find("img", src=True)
        images = re.findall(
            r"https://music-fa\.com/wp-content/uploads/.*?\.jpg", str(image_snippet)
        )
        music = article.find("span", class_="play")
        try:
            link_for_download = music["data-song"]
        except TypeError:
            link_for_download = None

        search_result.append(
            dict(
                title=title,
                images=images,
                link_for_download=link_for_download
            )
        )

    return {
        "success": True,
        "data": search_result
    }
