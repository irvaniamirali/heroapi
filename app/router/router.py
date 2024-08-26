from fastapi import APIRouter, Response, status

import asyncio

from typing import Optional

from app.router.tags import *

from app.router.api import ai
from app.router.api import duckduckgo
from app.router.api import translator

router = APIRouter(prefix="/api")


@router.get("/gpt", tags=AI, status_code=status.HTTP_200_OK)
@router.post("/gpt", tags=AI, status_code=status.HTTP_200_OK)
async def gpt(response: Response, query: str) -> dict:
    """
    ChatGPT 3.5 API.
    """
    return await ai.gpt(response, query)


@router.get("/duckduckgo/text", tags=DuckDuckGo, status_code=status.HTTP_200_OK)
@router.post("/duckduckgo/text", tags=DuckDuckGo, status_code=status.HTTP_200_OK)
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


@router.get("/translate", tags=Translate, status_code=status.HTTP_200_OK)
@router.get("/translate", tags=Translate, status_code=status.HTTP_200_OK)
async def translate(
        response: Response,
        text: str,
        to_lang: Optional[str] = "auto",
        from_lang: Optional[str] = "auto"
) -> dict:
    """
    Translation of texts based on the Google Translate engine.
    """
    return await translator.translate(response, text, to_lang, from_lang)
