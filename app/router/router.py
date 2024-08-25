from fastapi import APIRouter, Response, status

import asyncio

from typing import Optional

from app.router.api import ai
from app.router.api import duckduckgo

router = APIRouter(prefix="/api")


@router.get("/gpt", status_code=status.HTTP_200_OK)
@router.post("/gpt", status_code=status.HTTP_200_OK)
async def gpt(response: Response, query: str) -> dict:
    """
    ChatGPT 3.5 API.
    """
    return await ai.gpt(response, query)


@router.get("/duckduckgo/text", status_code=status.HTTP_200_OK)
@router.post("/duckduckgo/text", status_code=status.HTTP_200_OK)
async def duckduckgo_text(
        query: str,
        max_results: Optional[int] = 100,
        region: Optional[str] = "wt-wt",
        limit: Optional[str] = None
) -> dict:
    """
    DuckDuckGo text search. Query params: https://duckduckgo.com/params.
    """
    query_results = await asyncio.gather(duckduckgo.text_query(query, max_results, region, limit))
    return {
        "success": True,
        "data": query_results,
        "error_message": None
    }
