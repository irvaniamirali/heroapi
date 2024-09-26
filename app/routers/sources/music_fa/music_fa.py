from fastapi import APIRouter, status

from app.api.sources.music_fa import search

from typing import Optional

router = APIRouter(prefix="/api", tags=["Music search"])


@router.get("/music-fa", status_code=status.HTTP_200_OK)
async def music_fa(query: str, page: Optional[int] = 1) -> list:
    """
    Search and search web service on the [music-fa](https://music-fa.com) site.
    """
    return await search(query, page)
