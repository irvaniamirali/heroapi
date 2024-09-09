from fastapi import APIRouter, Response, status

from typing import Optional

from app.api.sources.others_api import icon_search, language_detect_api, convert_html_to_json_api

router = APIRouter(prefix="/api")


@router.get("/icon", tags=["Icon search"], status_code=status.HTTP_200_OK)
@router.post("/icon", tags=["Icon search"], status_code=status.HTTP_200_OK)
async def icons(query: str, page: Optional[int] = 1) -> dict:
    """
    Web Service to search icon from [icon-icons](https://icon-icons.com)
    """
    return await icon_search(query, page)


@router.get("/lang", tags=["Language detect"], status_code=status.HTTP_200_OK)
@router.post("/lang", tags=["Language detect"], status_code=status.HTTP_200_OK)
async def language_detect(response: Response, text: str) -> dict:
    """
    Identifying the language of texts
    """
    return await language_detect_api(response, text)


@router.get("/html2json", tags=["Convert HTML to JSON"], status_code=status.HTTP_200_OK)
@router.post("/html2json", tags=["Convert HTML to JSON"], status_code=status.HTTP_200_OK)
async def convert_html_to_json(html: str) -> dict:
    """
    Convert HTML document to json
    """
    return await convert_html_to_json_api(html)
