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
    query_result = await ai.gpt(response, query)
    return {
        "success": True,
        "data": query_result,
        "error_message": None
    }


@router.get("/duckduckgo/text", tags=DuckDuckGo, status_code=status.HTTP_200_OK)
@router.post("/duckduckgo/text", tags=DuckDuckGo, status_code=status.HTTP_200_OK)
async def duckduckgo_text(
        query: str,
        region: Optional[str] = "wt-wt",
        safe_search: Optional[str] = None,
        timelimit: Optional[str] = None,
        max_results: Optional[int] = 100,
) -> dict:
    """
    DuckDuckGo text search. Query params: https://duckduckgo.com/params.
    Args:
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safe_search: on, moderate, off. Defaults to "moderate".
        timelimit: d, w, m, y. Defaults to None.
        max_results: max number of results. If None, returns results only from the first response.

    Returns:
        List of dictionaries with search results, or None if there was an error.
    """
    query_results = await asyncio.gather(
        duckduckgo.text_query(
            query, region, safe_search, timelimit, "api", max_results
        )
    )
    return {
        "success": True,
        "data": query_results,
        "error_message": None
    }


@router.get("/duckduckgo/text/html", tags=DuckDuckGo, status_code=status.HTTP_200_OK)
@router.post("/duckduckgo/text/html", tags=DuckDuckGo, status_code=status.HTTP_200_OK)
async def duckduckgo_html_text(
        query: str,
        region: Optional[str] = "wt-wt",
        safe_search: Optional[str] = None,
        timelimit: Optional[str] = None,
        max_results: Optional[int] = 100,
) -> dict:
    """
    DuckDuckGo text search. backend to HTML. Query params: https://duckduckgo.com/params.
    """
    query_results = await asyncio.gather(
        duckduckgo.text_query(
            query, region, safe_search, timelimit, "html", max_results
        )
    )
    return {
        "success": True,
        "data": query_results,
        "error_message": None
    }


@router.get("/duckduckgo/text/lite", tags=DuckDuckGo, status_code=status.HTTP_200_OK)
@router.post("/duckduckgo/text/lite", tags=DuckDuckGo, status_code=status.HTTP_200_OK)
async def duckduckgo_lite_text(
        query: str,
        region: Optional[str] = "wt-wt",
        safe_search: Optional[str] = None,
        timelimit: Optional[str] = None,
        max_results: Optional[int] = 100,
) -> dict:
    """
    DuckDuckGo text search. backend to LITE. Query params: https://duckduckgo.com/params.
    """
    query_results = await asyncio.gather(
        duckduckgo.text_query(
            query, region, safe_search, timelimit, "lite", max_results
        )
    )
    return {
        "success": True,
        "data": query_results,
        "error_message": None
    }


@router.get("/duckduckgo/translate", tags=DuckDuckGo + Translate, status_code=status.HTTP_200_OK)
@router.post("/duckduckgo/translate", tags=DuckDuckGo + Translate, status_code=status.HTTP_200_OK)
async def duckduckgo_translate(
        text: str,
        from_lang: Optional[str] = None,
        to_lang: Optional[str] = "en"
) -> dict:
    """
    DuckDuckGo translate API
    """
    query_results = await asyncio.gather(duckduckgo.translate(text, from_lang, to_lang))
    return {
        "success": True,
        "data": query_results,
        "error_message": None
    }


@router.get("/duckduckgo/news", tags=DuckDuckGo, status_code=status.HTTP_200_OK)
@router.post("/duckduckgo/news", tags=DuckDuckGo, status_code=status.HTTP_200_OK)
async def duckduckgo_news(
        query: str,
        max_results: Optional[int] = 10,
        region: Optional[str] = None,
        safe_search: Optional[str] = "moderate",
        timelimit: Optional[str] = None
):
    """
    DuckDuckGo news search. Query params: https://duckduckgo.com/params.
    Args:
        query: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safe_search: on, moderate, off. Defaults to "moderate".
        timelimit: d, w, m. Defaults to None.
        max_results: max number of results. If None, returns results only from the first response.
    Returns:
        List of dictionaries with news search results.
    """
    query_result = await asyncio.gather(
        duckduckgo.news(
            query, max_results, region, safe_search, timelimit
        )
    )
    return {
        "success": True,
        "data": query_result,
        "error_message": None
    }


@router.get("/duckduckgo/chat", tags=DuckDuckGo + AI, status_code=status.HTTP_200_OK)
@router.post("/duckduckgo/chat", tags=DuckDuckGo + AI, status_code=status.HTTP_200_OK)
async def duckduckgo_chat(
        query: str,
        model: Optional[str] = "gpt-4o-mini",
        timeout: Optional[int] = 30,
):
    """
    DuckDuckGo AI chat. Query params: https://duckduckgo.com/params.
    models: "gpt-4o-mini", "claude-3-haiku", "llama-3.1-70b", "mixtral-8x7b".
    """
    query_result = await asyncio.gather(duckduckgo.chat(query, model, timeout))
    return {
        "success": True,
        "data": query_result,
        "error_message": None
    }


@router.get("/duckduckgo/images", tags=DuckDuckGo, status_code=status.HTTP_200_OK)
@router.post("/duckduckgo/images", tags=DuckDuckGo, status_code=status.HTTP_200_OK)
async def duckduckgo_images(
        query: str,
        max_results: Optional[int] = 100,
        region: Optional[str] = "wt-wt",
        timelimit: Optional[str] = None,
        size: Optional[str] = None,
        color: Optional[str] = None,
        type_image: Optional[str] = None,
        layout: Optional[str] = None,
        license_image: Optional[str] = None
):
    """
    DuckDuckGo images search. Query params: https://duckduckgo.com/params.
    Args:
        max_results: max number of results. If None, returns results only from the first response.
        layout: Square, Tall, Wide. Defaults to None.
        region: wt-wt, us-en, uk-en, ru-ru, etc.
        timelimit: Day, Week, Month, Year. Defaults to None.
        size: Small, Medium, Large, Wallpaper.
        color: color, Monochrome, Red, Orange, Yellow, Green, Blue etc.
        type_image: photo, clipart, gif, transparent, line.
        license_image: any (All Creative Commons), Public (PublicDomain),
            Share (Free to Share and Use), ShareCommercially (Free to Share and Use Commercially),
            Modify (Free to Modify, Share, and Use), ModifyCommercially (Free to Modify, Share, and
            Use Commercially). Defaults to None.
    Returns:
        List of dictionaries with images search results.
    """
    query_result = await asyncio.gather(
        duckduckgo.images(
            query, max_results, region, timelimit, size, color, type_image, layout, license_image
        )
    )
    return {
        "success": True,
        "data": query_result,
        "error_message": None
    }


@router.get("/duckduckgo/maps", tags=DuckDuckGo, status_code=status.HTTP_200_OK)
@router.post("/duckduckgo/maps", tags=DuckDuckGo, status_code=status.HTTP_200_OK)
async def duckduckgo_maps(
        query: str,
        place: Optional[str] = None,
        street: Optional[str] = None,
        city: Optional[str] = None,
        county: Optional[str] = None,
        state: Optional[str] = None,
        country: Optional[str] = None,
        postalcode: Optional[str] = None,
        latitude: Optional[str] = None,
        longitude: Optional[str] = None,
        radius: Optional[int] = 0,
        max_results: Optional[int] = 100
) -> dict:
    """
    DuckDuckGo maps search. Query params: https://duckduckgo.com/params.
    Args:
        query: keywords for query
        place: if set, the other parameters are not used.
        street: house number/street.
        city: city of search.
        county: county of search.
        state: state of search.
        country: country of search.
        postalcode: postalcode of search.
        latitude: geographic coordinate (north-south position).
        longitude: geographic coordinate (east-west position); if latitude and
            longitude are set, the other parameters are not used.
        radius: expand the search square by the distance in kilometers.
        max_results: max number of results. If None, returns results only from the first response.

    Returns:
        List of dictionaries with maps search results, or None if there was an error.
    """
    query_results = await asyncio.gather(
        duckduckgo.maps(
            query, place, street, city, county, state, country, postalcode, latitude, longitude, radius, max_results
        )
    )
    return {
        "success": True,
        "data": query_results,
        "error_message": None
    }


@router.get("/translate", tags=Translate, status_code=status.HTTP_200_OK)
@router.post("/translate", tags=Translate, status_code=status.HTTP_200_OK)
async def translate(
        response: Response,
        text: str,
        to_lang: Optional[str] = "auto",
        from_lang: Optional[str] = "auto"
) -> dict:
    """
    Translation of texts based on the Google Translate engine.
    """
    text_result = await translator.translate(response, text, to_lang, from_lang)
    return {
        "success": True,
        "data": text_result,
        "error_message": None
    }
