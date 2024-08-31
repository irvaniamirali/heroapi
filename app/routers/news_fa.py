from fastapi import APIRouter, status

from app.api.sources.news_fa import news_v1, news_v2

from typing import Optional

router = APIRouter(prefix="/api/news", tags=["News"])


@router.get("/v1", status_code=status.HTTP_200_OK)
@router.post("/v1", status_code=status.HTTP_200_OK)
async def news(page: Optional[int] = 1) -> dict:
    """
    Web service to display news. onnected to the site www.tasnimnews.com
    """
    return await news_v1(page)


@router.get("/v2", status_code=status.HTTP_200_OK)
@router.post("/v2", status_code=status.HTTP_200_OK)
async def news_v2(page: Optional[int] = 1) -> dict:
    """
    Web service, the latest technological news. `page` parameter has 6000 pages
    """
    return await news_v2(page)
