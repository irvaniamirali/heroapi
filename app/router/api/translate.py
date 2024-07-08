from fastapi import APIRouter, Response, status

from typing import Optional

import urllib.parse
import html
import re

import httpx

client = httpx.AsyncClient()

router = APIRouter(prefix="/api", tags=["Translate"])


@router.get("/translate", status_code=status.HTTP_200_OK)
@router.post("/translate", status_code=status.HTTP_200_OK)
async def translate(
        response: Response,
        text: str,
        to_lang: Optional[str] = "auto",
        from_lang: Optional[str] = "auto"
) -> dict:
    """
    Translation of texts based on the Google Translate engine
    """
    url = "https://translate.google.com"
    query_url = f"{url}/m?tl={to_lang}&sl={from_lang}&q={urllib.parse.quote(text)}"
    req = await client.request(
        method="GET", url=query_url, headers={
            "User-Agent":
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0"
        }
    )
    if req.status_code != httpx.codes.OK:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "error_message": "A problem has occurred on our end"
        }

    translated_text = re.findall(r'(?s)class="(?:t0|result-container)">(.*?)<', request.text)
    result = html.unescape(translated_text[0])
    return {
        "success": True,
        "data": result
    }
