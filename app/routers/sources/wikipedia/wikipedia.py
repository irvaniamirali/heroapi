from fastapi import APIRouter, Response, status

from typing import Optional

from app.api.sources.wikipedia import search

router = APIRouter(prefix="/api", tags=["WikiPedia article search"])


@router.get("/wikipedia/search", status_code=status.HTTP_200_OK)
@router.post("/wikipedia/search", status_code=status.HTTP_200_OK)
async def wikipedia(
        response: Response,
        query: str,
        lang: Optional[str] = "en",
        format: Optional[str] = None
) -> dict:
    """
    Do a Wikipedia search for `query`.
    """
    return await search(response, query, lang, format)
