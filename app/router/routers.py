from fastapi import APIRouter, Response, status

from typing import Optional

from app.router.tags import *

from app.router.api import ai
from app.router.api import base64_api
from app.router.api import datetime_api
from app.router.api import duckduckgo
from app.router.api import faker
from app.router.api import github
from app.router.api import lexica_api
from app.router.api import music_fa
from app.router.api import news_fa
from app.router.api import pypi_projects
from app.router.api import shop
from app.router.api import translator
from app.router.api import others_api

router = APIRouter(prefix="/api")


@router.get("/gpt", tags=AI, status_code=status.HTTP_200_OK)
@router.post("/gpt", tags=AI, status_code=status.HTTP_200_OK)
async def gpt(response: Response, query: str) -> dict:
    """
    ChatGPT 3.5 API.
    """
    return await ai.gpt(response, query)


@router.get("/bs64encode", tags=Base64, status_code=status.HTTP_200_OK)
@router.post("/bs64encode", tags=Base64, status_code=status.HTTP_200_OK)
async def base64encode(string: str) -> dict:
    """
    Encode to Base64 format
    """
    return await base64_api.base64encode(string)


@router.get("/bs64decode", tags=Base64, status_code=status.HTTP_200_OK)
@router.post("/bs64decode", tags=Base64, status_code=status.HTTP_200_OK)
async def base64_decode(response: Response, string) -> dict:
    """
    Decode from Base64 format
    """
    return await base64_api.b64decode(response, string)


@router.get("/datetime/solar", tags=DateTime, status_code=status.HTTP_200_OK)
@router.post("/datetime/solar", tags=DateTime, status_code=status.HTTP_200_OK)
async def solar_datetime() -> dict:
    """
    Current Jalali date
    """
    return await datetime_api.solar_date()


@router.get("/datetime/ad", tags=DateTime, status_code=status.HTTP_200_OK)
@router.post("/datetime/ad", tags=DateTime, status_code=status.HTTP_200_OK)
async def ad_datetime() -> dict:
    """
    Current AD date
    """
    return await datetime_api.ad_date()


@router.get("/datetime/iso", tags=DateTime, status_code=status.HTTP_200_OK)
@router.post("/datetime/iso", tags=DateTime, status_code=status.HTTP_200_OK)
async def iso_date(year: int, month: int, day: int, prefix: Optional[str] = "/") -> dict:
    """
    Return the Jalali date as a string in ISO 8601 format.
    """
    return await datetime_api.iso_date(year, month, day, prefix)


@router.get("/datetime/convert-ad", tags=DateTime, status_code=status.HTTP_200_OK)
@router.post("/datetime/convert-ad", tags=DateTime, status_code=status.HTTP_200_OK)
async def convert_ad_to_jalali(year: int, month: int, day: int) -> dict:
    """
    Convert AD date to Jalali date.
    """
    return await datetime_api.convert_ad_to_jalali(year, month, day)


@router.get("/datetime/convert-jalali", tags=DateTime, status_code=status.HTTP_200_OK)
@router.post("/datetime/convert-jalali", tags=DateTime, status_code=status.HTTP_200_OK)
async def convert_jalali_to_ad(year: int, month: int, day: int) -> dict:
    """
    Convert Jalali date to AD date.
    """
    return await datetime_api.convert_jalali_to_ad(year, month, day)


@router.get("/faker/text", tags=FakeData, status_code=status.HTTP_200_OK)
@router.post("/faker/text", tags=FakeData, status_code=status.HTTP_200_OK)
async def faker_text(language: Optional[str] = "en") -> dict:
    """
    Random fake text API
    Only `en` and `fa` are available.
    """
    return await faker.text(language)


@router.get("/faker/name", tags=FakeData, status_code=status.HTTP_200_OK)
@router.post("/faker/name", tags=FakeData, status_code=status.HTTP_200_OK)
async def faker_name(count: Optional[int] = 20, language: Optional[str] = "en") -> list:
    """
    Random fake name API
    :language: Only `en` and `fa` are available.
    """
    return await faker.name(count, language)


@router.get("/faker/email", tags=FakeData, status_code=status.HTTP_200_OK)
@router.post("/faker/email", tags=FakeData, status_code=status.HTTP_200_OK)
async def faker_email(count: Optional[int] = 20) -> list:
    """
    Random fake email API
    """
    return await faker.email(count)


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
        query: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safe_search: on, moderate, off. Defaults to "moderate".
        timelimit: d, w, m, y. Defaults to None.
        max_results: max number of results. If None, returns results only from the first response.

    Returns:
        List of dictionaries with search results, or None if there was an error.
    """
    return await duckduckgo.text_query(query, region, safe_search, timelimit, "api", max_results)


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
    return await duckduckgo.text_query(query, region, safe_search, timelimit, "html", max_results)


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
    return await duckduckgo.text_query(query, region, safe_search, timelimit, "lite", max_results)


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
    return await duckduckgo.translate(text, from_lang, to_lang)


@router.get("/duckduckgo/news", tags=DuckDuckGo, status_code=status.HTTP_200_OK)
@router.post("/duckduckgo/news", tags=DuckDuckGo, status_code=status.HTTP_200_OK)
async def duckduckgo_news(
        query: str,
        max_results: Optional[int] = 10,
        region: Optional[str] = None,
        safe_search: Optional[str] = "moderate",
        timelimit: Optional[str] = None
) -> dict:
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
    return await duckduckgo.news(query, max_results, region, safe_search, timelimit)


@router.get("/duckduckgo/chat", tags=DuckDuckGo + AI, status_code=status.HTTP_200_OK)
@router.post("/duckduckgo/chat", tags=DuckDuckGo + AI, status_code=status.HTTP_200_OK)
async def duckduckgo_chat(
        query: str,
        model: Optional[str] = "gpt-4o-mini",
        timeout: Optional[int] = 30,
) -> dict:
    """
    DuckDuckGo AI chat. Query params: https://duckduckgo.com/params.
    models: "gpt-4o-mini", "claude-3-haiku", "llama-3.1-70b", "mixtral-8x7b".
    """
    return await duckduckgo.chat(query, model, timeout)


@router.get("/duckduckgo/images", tags=DuckDuckGo, status_code=status.HTTP_200_OK)
@router.post("/duckduckgo/images", tags=DuckDuckGo, status_code=status.HTTP_200_OK)
async def duckduckgo_images(
        query: str,
        region: Optional[str] = "wt-wt",
        timelimit: Optional[str] = None,
        size: Optional[str] = None,
        color: Optional[str] = None,
        type_image: Optional[str] = None,
        layout: Optional[str] = None,
        license_image: Optional[str] = None,
        max_results: Optional[int] = 100
) -> dict:
    """
    DuckDuckGo images search. Query params: https://duckduckgo.com/params.
    Args:
        query: keywords for query.
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
        max_results: max number of results. If None, returns results only from the first response.
    Returns:
        List of dictionaries with images search results.
    """
    return await duckduckgo.images(query, region, timelimit, size, color, type_image, layout, license_image, max_results)


@router.get("/duckduckgo/videos", tags=DuckDuckGo, status_code=status.HTTP_200_OK)
@router.post("/duckduckgo/videos", tags=DuckDuckGo, status_code=status.HTTP_200_OK)
async def duckduckgo_videos(
        query: str,
        region: Optional[str] = "wt-wt",
        safe_search: Optional[str] = "moderate",
        timelimit: Optional[str] = None,
        resolution: Optional[str] = None,
        duration: Optional[str] = None,
        license_videos: Optional[str] = None,
        max_results: Optional[str] = None,
) -> dict:
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
    return await duckduckgo.videos(query, region, safe_search, timelimit, resolution, duration, license_videos, max_results)


@router.get("/api/duckduckgo/answers", tags=DuckDuckGo, status_code=status.HTTP_200_OK)
@router.post("/api/duckduckgo/answers", tags=DuckDuckGo, status_code=status.HTTP_200_OK)
async def duckduckgo_answers(query: str) -> dict:
    """
    DuckDuckGo instant answers. Query params: https://duckduckgo.com/params.
    """
    return await duckduckgo.answers(query)


@router.get("/duckduckgo/suggestions", tags=DuckDuckGo, status_code=status.HTTP_200_OK)
@router.post("/duckduckgo/suggestions", tags=DuckDuckGo, status_code=status.HTTP_200_OK)
async def duckduckgo_suggestions(query: str, region: Optional[str] = "wt-wt") -> dict:
    """
    DuckDuckGo suggestions. Query params: https://duckduckgo.com/params.

    Args:
        query: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".

    Returns:
        List of dictionaries with suggestions results.
    """
    return await duckduckgo.suggestions(query, region)


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
    return await duckduckgo.maps(
        query, place, street, city, county, state, country, postalcode, latitude, longitude, radius, max_results
    )


@router.get("/github/topic", tags=GitHub, status_code=status.HTTP_200_OK)
@router.post("/github/topic", tags=GitHub, status_code=status.HTTP_200_OK)
async def github_topic_search(query: str, per_page: Optional[int] = 30, page: Optional[int] = 1) -> dict:
    """
    GitHub topic search web service
    """
    return await github.topic_search(query, per_page, page)


@router.get("/github/repo", tags=GitHub, status_code=status.HTTP_200_OK)
@router.post("/github/repo", tags=GitHub, status_code=status.HTTP_200_OK)
async def github_repo_search(
        name: str,
        sort: Optional[str] = "stars",
        order: Optional[str] = "desc",
        per_page: Optional[int] = 30,
        page: Optional[int] = 1
) -> dict:
    """
    GitHub repository search web service.
    sort list repository: "stars", "forks", "help-wanted-issues", "updated".
    """
    return await github.repo_search(name, sort, order, per_page, page)


@router.get("/github/users", tags=GitHub, status_code=status.HTTP_200_OK)
async def github_users_search(
        query: str,
        sort: Optional[str] = "followers",
        order: Optional[str] = "desc",
        per_page: Optional[int] = 30,
        page: Optional[int] = 1,
) -> dict:
    """
    GitHub users search web service.
    sort list repository: "followers", "repositories", "joined".
    """
    return await github.users_search(query, sort, order, per_page, page)


@router.get("/lexica", tags=AI_Image + AI, status_code=status.HTTP_200_OK)
@router.post("/lexica", tags=AI_Image + AI, status_code=status.HTTP_200_OK)
async def lexica(response: Response, query: str) -> dict:
    """
    AI Image Generator. [lexica](lexica.art)
    """
    return await lexica_api.image(response, query)


@router.get("/music-fa", tags=Music, status_code=status.HTTP_200_OK)
@router.post("/music-fa", tags=Music, status_code=status.HTTP_200_OK)
async def music_fa(query: str, page: Optional[int] = 1) -> dict:
    """
    Search and search web service on the [music-fa](https://music-fa.com) site.
    """
    return await music_fa.search(query, page)


@router.get("/news/v1", tags=News, status_code=status.HTTP_200_OK)
@router.post("/news/v1", tags=News, status_code=status.HTTP_200_OK)
async def news(page: Optional[int] = 1) -> dict:
    """
    Web service to display news. onnected to the site www.tasnimnews.com
    """
    return await news_fa.news_v1(page)


@router.get("/news/v2", tags=News, status_code=status.HTTP_200_OK)
@router.post("/news/v2", tags=News, status_code=status.HTTP_200_OK)
async def news_v2(page: Optional[int] = 1) -> dict:
    """
    Web service, the latest technological news. `page` parameter has 6000 pages
    """
    return await news_fa.news_v2(page)


@router.get("/icon", tags=Icons, status_code=status.HTTP_200_OK)
@router.post("/icon", tags=Icons, status_code=status.HTTP_200_OK)
async def icons_search(query: str, page: Optional[int] = 1) -> dict:
    """
    Web Service to search icon from [icon-icons](https://icon-icons.com)
    """
    return await others_api.icon_search(query, page)


@router.get("/lang", tags=Language, status_code=status.HTTP_200_OK)
@router.post("/lang", tags=Language, status_code=status.HTTP_200_OK)
async def language_detect(response: Response, text: str) -> dict:
    """
    Identifying the language of texts
    """
    return await others_api.language_detect(response, text)


@router.get("/html2json", tags=HTML2JSON, status_code=status.HTTP_200_OK)
@router.post("/html2json", tags=HTML2JSON, status_code=status.HTTP_200_OK)
async def convert_html_to_json(html: str) -> dict:
    """
    Convert HTML document to json
    """
    return await others_api.convert_html_to_json(html)


@router.get("/pypi", tags=PyPi, status_code=status.HTTP_200_OK)
@router.post("/pypi", tags=PyPi, status_code=status.HTTP_200_OK)
async def pypi_projects_search(name: str) -> dict:
    """
    PyPi package search web service
    """
    return await pypi_projects.package_search(name)


@router.get("/divar", tags=Divar, status_code=status.HTTP_200_OK)
@router.post("/divar", tags=Divar, status_code=status.HTTP_200_OK)
async def divar_product_search(query: str, city: Optional[str] = "tehran") -> dict:
    """
    Web search service in [Divar](https://divar.ir).
    """
    return await shop.divar(query, city)


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
    return await translator.translate(response, text, to_lang, from_lang)
