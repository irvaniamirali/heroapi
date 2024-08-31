from fastapi import APIRouter, Response, status

from typing import Optional

from bs4 import BeautifulSoup

import html_to_json
import langdetect

from httpx import AsyncClient, codes

client = AsyncClient()

BASE_URL = "https://icon-icons.com"


async def icon_search(query, page):
    request = await client.request("GET", url=f"{BASE_URL}/search/icons/?filtro={query}&page={page}")
    soup = BeautifulSoup(request.text, "html.parser")
    icons = soup.find_all("div", class_="icon-preview")

    search_result = []
    for icon in icons:
        data_original = icon.find("img", loading="lazy", src=True)
        search_result.append(data_original.get("src"))

    return {
        "success": True,
        "data": search_result,
        "error_message": None
    }


async def language_detect_api(response, text):
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


async def convert_html_to_json_api(html):
    """
    Convert HTML document to json
    """
    output_json = html_to_json.convert(html)
    return {
        "success": True,
        "data": output_json,
        "error_message": None
    }
