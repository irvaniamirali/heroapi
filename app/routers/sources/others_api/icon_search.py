from fastapi import APIRouter, status

from typing import Optional

from app.api.sources.others_api import icon_search

router = APIRouter(prefix="/api")


@router.get("/icon", tags=["Icon search"], status_code=status.HTTP_200_OK)
async def icons(query: str, page: Optional[int] = 1) -> list:
    """
    Web Service to search icon from [icon-icons](https://icon-icons.com)
    """
    return await icon_search(query, page)
