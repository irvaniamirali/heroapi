from fastapi import APIRouter, status

from app.api.sources.duckduckgo import (
    text_query, news, chat, images, videos, answers, suggestions, translate, maps
)

from typing import Optional

router = APIRouter(prefix="/api/duckduckgo", tags=["DuckDuckGo"])


@router.get("/text", status_code=status.HTTP_200_OK)
async def duckduckgo_text(
        query: str,
        region: Optional[str] = "wt-wt",
        safe_search: Optional[str] = "moderate",
        timelimit: Optional[str] = None,
        max_results: Optional[int] = 100,
) -> list:
    """
    DuckDuckGo text search. Query params: https://duckduckgo.com/params.
    Args:
        query: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safe_search: on, moderate, off. Defaults to "moderate".
        timelimit: d, w, m, y. Defaults to None.
        max_results: max number of results. If None, returns results only from the first response.

    Returns:
        List of dictionaries with search results, or None if there was an error.
    """
    return await text_query(query, region, safe_search, timelimit, "api", max_results)


@router.post("/text/html", status_code=status.HTTP_200_OK)
async def duckduckgo_html_text(
        query: str,
        region: Optional[str] = "wt-wt",
        safe_search: Optional[str] = "moderate",
        timelimit: Optional[str] = None,
        max_results: Optional[int] = 100,
) -> list:
    """
    DuckDuckGo text search. backend to HTML. Query params: https://duckduckgo.com/params.
    """
    return await text_query(query, region, safe_search, timelimit, "html", max_results)


@router.post("/text/lite", status_code=status.HTTP_200_OK)
async def duckduckgo_lite_text(
        query: str,
        region: Optional[str] = "wt-wt",
        safe_search: Optional[str] = "moderate",
        timelimit: Optional[str] = None,
        max_results: Optional[int] = 100,
) -> list:
    """
    DuckDuckGo text search. backend to LITE. Query params: https://duckduckgo.com/params.
    """
    return await text_query(query, region, safe_search, timelimit, "lite", max_results)


@router.post("/translate", tags=["Translate"], status_code=status.HTTP_200_OK)
async def duckduckgo_translate(
        text: str,
        from_lang: Optional[str] = None,
        to_lang: Optional[str] = "en"
) -> list:
    """
    DuckDuckGo translate API
    """
    return await translate(text, from_lang, to_lang)


@router.get("/news", status_code=status.HTTP_200_OK)
async def duckduckgo_news(
        query: str,
        max_results: Optional[int] = 10,
        region: Optional[str] = None,
        safe_search: Optional[str] = "moderate",
        timelimit: Optional[str] = None
) -> list:
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
    return await news(query, max_results, region, safe_search, timelimit)


@router.get("/images", status_code=status.HTTP_200_OK)
async def duckduckgo_images(
        query: str,
        region: Optional[str] = "wt-wt",
        safesearch: Optional[str] = "moderate",
        timelimit: Optional[str] = None,
        size: Optional[str] = None,
        color: Optional[str] = None,
        type_image: Optional[str] = None,
        layout: Optional[str] = None,
        license_image: Optional[str] = None,
        max_results: Optional[int] = 100
) -> list:
    """
    DuckDuckGo images search. Query params: https://duckduckgo.com/params.
    Args:
        query: keywords for query.
        layout: Square, Tall, Wide. Defaults to None.
        safesearch: on, moderate, off. Defaults to "moderate".
        region: wt-wt, us-en, uk-en, ru-ru, etc.
        timelimit: Day, Week, Month, Year. Defaults to None.
        size: Small, Medium, Large, Wallpaper.
        color: color, Monochrome, Red, Orange, Yellow, Green, Blue etc.
        type_image: photo, clipart, gif, transparent, line.
        license_image: any (All Creative Commons), Public (PublicDomain),
            Share (Free to Share and Use), ShareCommercially (Free to Share and Use Commercially),
            Modify (Free to Modify, Share, and Use), ModifyCommercially (Free to Modify, Share, and
            Use Commercially). Defaults to None.
        max_results: max number of results. If None, returns results only from the first response.
    Returns:
        List of dictionaries with images search results.
    """
    return await images(query, region, safesearch, timelimit, size, color, type_image, layout, license_image, max_results)


@router.get("/chat", tags=["AI"], status_code=status.HTTP_200_OK)
async def duckduckgo_chat(
        query: str,
        model: Optional[str] = "gpt-4o-mini",
        timeout: Optional[int] = 30,
) -> dict:
    """
    DuckDuckGo AI chat. Query params: https://duckduckgo.com/params.
    models: "gpt-4o-mini", "claude-3-haiku", "llama-3.1-70b", "mixtral-8x7b".
    """
    return await chat(query, model, timeout)


@router.get("/videos", status_code=status.HTTP_200_OK)
async def duckduckgo_videos(
        query: str,
        region: Optional[str] = "wt-wt",
        safe_search: Optional[str] = "moderate",
        timelimit: Optional[str] = None,
        resolution: Optional[str] = None,
        duration: Optional[str] = None,
        license_videos: Optional[str] = None,
        max_results: Optional[int] = None,
) -> list:
    """
    DuckDuckGo videos search. Query params: https://duckduckgo.com/params.
    Args:
        query: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc.
        safe_search: on, moderate, off.
        timelimit: d, w, m.
        resolution: high, standart.
        duration: short, medium, long.
        license_videos: creativeCommon, youtube.
        max_results: max number of results. If None, returns results only from the first response.

    Returns:
        List of dictionaries with videos search results.
    """
    return await videos(query, region, safe_search, timelimit, resolution, duration, license_videos, max_results)


@router.get("/answers", status_code=status.HTTP_200_OK)
async def duckduckgo_answers(query: str) -> list:
    """
    DuckDuckGo instant answers. Query params: https://duckduckgo.com/params.
    """
    return await answers(query)


@router.get("/suggestions", status_code=status.HTTP_200_OK)
async def duckduckgo_suggestions(query: str, region: Optional[str] = "wt-wt") -> list:
    """
    DuckDuckGo suggestions. Query params: https://duckduckgo.com/params.

    Args:
        query: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".

    Returns:
        List of dictionaries with suggestions results.
    """
    return await suggestions(query, region)


@router.get("/maps", status_code=status.HTTP_200_OK)
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
) -> list:
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
    return await maps(
        query, place, street, city, county, state, country, postalcode, latitude, longitude, radius, max_results
    )
