from fastapi import APIRouter, status

from typing import Optional

import asyncio

from duckduckgo_search import AsyncDDGS

router = APIRouter(prefix="/duckduckgo", tags=["DuckDuckGo"])


async def text_query(word, max_results, region, limit):
    return await AsyncDDGS(proxy=None).atext(
        word, max_results=max_results, region=region, timelimit=limit
    )


async def news(query, max_results, region, limit):
    return await AsyncDDGS(proxy=None).anews(
        query, max_results=max_results, region=region, timelimit=limit
    )


async def chat(query, model, timeout):
    return await AsyncDDGS(proxy=None).achat(query, model=model, timeout=timeout)


async def images(query, max_results, region, limit, size, color, type_image, layout, license_image):
    return await AsyncDDGS(proxy=None).aimages(
        query,
        max_results=max_results,
        region=region,
        timelimit=limit,
        size=size,
        color=color,
        type_image=type_image,
        layout=layout,
        license_image=license_image
    )


async def translate(text, from_lang, to_lang):
    return await AsyncDDGS(proxy=None).atranslate(text, from_=from_lang, to=to_lang)


async def maps(
        query, place, street, city, county, state, country,
        postalcode, latitude, longitude, radius, max_results
):
    return await AsyncDDGS(proxy=None).amaps(
        query, place, street, city, county, state, country,
        postalcode, latitude, longitude, radius, max_results
    )


@router.get("/text", status_code=status.HTTP_200_OK)
@router.post("/text", status_code=status.HTTP_200_OK)
async def duckduckgo_text(
        query: str,
        max_results: Optional[int] = 100,
        region: Optional[str] = "wt-wt",
        limit: Optional[str] = None
) -> dict:
    """
    DuckDuckGo text search API
    """
    query_results = await asyncio.gather(text_query(query, max_results, region, limit))
    return {
        "success": True,
        "data": query_results,
        "error_message": None
    }


@router.get("/news", status_code=status.HTTP_200_OK)
@router.post("/news", status_code=status.HTTP_200_OK)
async def duckduckgo_news(
        query: str,
        max_results: Optional[int] = 100,
        region: Optional[str] = "wt-wt",
        limit: Optional[str] = None
) -> dict:
    """
    DuckDuckGo news API
    """
    query_results = await asyncio.gather(news(query, max_results, region, limit))
    return {
        "success": True,
        "data": query_results,
        "error_message": None
    }


@router.get("/chat", tags=["AI"], status_code=status.HTTP_200_OK)
@router.post("/chat", tags=["AI"], status_code=status.HTTP_200_OK)
async def duckduckgo_chat(
        query: str,
        model: Optional[str] = "gpt-4o-mini",
        timeout: Optional[int] = 30
) -> dict:
    """
    DuckDuckGo chat API
    """
    query_results = await asyncio.gather(chat(query, model, timeout))
    return {
        "success": True,
        "data": query_results,
        "error_message": None
    }


@router.get("/images", status_code=status.HTTP_200_OK)
@router.post("/images", status_code=status.HTTP_200_OK)
async def duckduckgo_images(
        query: str,
        max_results: Optional[int] = 100,
        region: Optional[str] = "wt-wt",
        limit: Optional[str] = None,
        size: Optional[str] = None,
        color: Optional[str] = None,
        type_image: Optional[str] = None,
        layout: Optional[str] = None,
        license_image: Optional[str] = None
) -> dict:
    """
    DuckDuckGo image search API
    """
    query_results = await asyncio.gather(
        images(query, max_results, region, limit, size, color, type_image, layout, license_image)
    )
    return {
        "success": True,
        "data": query_results,
        "error_message": None
    }


@router.get("/translate", status_code=status.HTTP_200_OK)
@router.post("/translate", status_code=status.HTTP_200_OK)
async def duckduckgo_translate(
        text: str,
        from_lang: Optional[str] = None,
        to_lang: Optional[str] = "en"
) -> dict:
    """
    DuckDuckGo translate API
    """
    query_results = await asyncio.gather(translate(text, from_lang, to_lang))
    return {
        "success": True,
        "data": query_results,
        "error_message": None
    }


@router.get("/maps", status_code=status.HTTP_200_OK)
@router.post("/maps", status_code=status.HTTP_200_OK)
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
    DuckDuckGo maps API
    """
    query_results = await asyncio.gather(
        maps(
            query, place, street, city, county, state, country,
            postalcode, latitude, longitude, radius, max_results
        )
    )
    return {
        "success": True,
        "data": query_results,
        "error_message": None
    }
