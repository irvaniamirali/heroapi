from fastapi import APIRouter, status

from typing import Optional

from app.api.sources.wikipedia import search

router = APIRouter(prefix="/api", tags=["WikiPedia article search"])


@router.get("/wikipedia/search", status_code=status.HTTP_200_OK)
@router.post("/wikipedia/search", status_code=status.HTTP_200_OK)
async def wikipedia(query: str, lang: Optional[str] = "en", _format: Optional[str] = None) -> dict:
    """
    Do a Wikipedia search for `query`.
    """
    return await search(query, lang, _format)
