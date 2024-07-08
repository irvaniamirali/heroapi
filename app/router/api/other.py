from fastapi import APIRouter, Response, status

from typing import Optional

from bs4 import BeautifulSoup

import html_to_json
import langdetect

import httpx

client = httpx.AsyncClient()

router = APIRouter(prefix="/api")


@router.get("/icon", tags=["Icon Search"], status_code=status.HTTP_200_OK)
@router.post("/icon", tags=["Icon Search"], status_code=status.HTTP_200_OK)
async def icon_search(response: Response, query: str, page: Optional[int] = 1) -> dict:
    """
    Web Service to search icon from [icon-icons](https://icon-icons.com)
    """
    req = await client.request(
        method="GET", url=f"https://icon-icons.com/search/icons/?filtro={query}&page={page}"
    )
    if req.status_code != httpx.codes.OK:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "error_message": "A problem has occurred on our end"
        }

    soup = BeautifulSoup(req.text, "html.parser")
    icons = soup.find_all("div", class_="icon-preview")
    search_result = list()
    for icon in icons:
        data_original = icon.find("img", loading="lazy", src=True)
        search_result.append(data_original.get("src"))

    return {
        "success": True,
        "data": search_result
    }


@router.get("/lang", tags=["Language Detect"], status_code=status.HTTP_200_OK)
@router.post("/lang", tags=["Language Detect"], status_code=status.HTTP_200_OK)
async def language_detect(response: Response, text: str) -> dict:
    """
    Identifying the language of texts
    """
    try:
        result_detected = langdetect.detect(text)
        return {
            "success": True,
            "data": result_detected
        }
    except langdetect.LangDetectException:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "success": False,
            "error_message": "The value of the `text` parameter is not invalid"
        }


@router.get("/food/v1", tags=["Food search"], status_code=status.HTTP_200_OK)
@router.post("/food/v1", tags=["Food search"], status_code=status.HTTP_200_OK)
async def food_search(response: Response, query: str) -> dict:
    base_url = "https://mamifood.org"
    req = await client.request(
        method="GET", url=base_url + f"/cooking-training/search/{query}"
    )
    if req.status_code != httpx.codes.OK:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "error_message": "A problem has occurred on our end"
        }

    soup = BeautifulSoup(req.text, "html.parser")
    articles = soup.find_all("article", id="Table", class_="box m-box col3")

    final_values = list()
    for article in articles:
        image_box = article.find("img", class_="box-img")
        post_info = article.find("a", id="lnkimg", class_="a-img-box")
        post_date = article.find("div", id="Date", class_="inline-block").text

        image_url = base_url + image_box.get("src")
        post_url = post_info.get("href")
        food_title = image_box.get("title")
        final_values.append(
            dict(image_url=image_url, post_url=post_url, food_title=food_title, post_date=post_date)
        )

    return {
        "success": True,
        "data": final_values
    }


@router.get("/domain-price", tags=["Domain search"], status_code=status.HTTP_200_OK)
@router.post("/domain-price", tags=["Domain search"], status_code=status.HTTP_200_OK)
async def domain_price(response: Response) -> dict:
    """
    Get Domain price from [parsvds.com](https://parsvds.com) web site
    """
    req = await client.request(method="GET", url=f"https://parsvds.com/domain/")
    if req.status_code != httpx.codes.OK:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "error_message": "A problem has occurred on our end"
        }

    soup = BeautifulSoup(req.text, "html.parser")
    table_rows = soup.find_all("tr")

    search_result = list()
    for row in table_rows[1:]:
        domain = row.find_all("td")
        price = row.find_all("td")
        search_result.append(
            dict(
                domain=domain[0].text, price=price[1].text
            )
        )

    return {
        "success": True,
        "data": search_result
    }


@router.get("/html2json", tags=["Convert HTML to JSON"], status_code=status.HTTP_200_OK)
@router.post("/html2json", tags=["Convert HTML to JSON"], status_code=status.HTTP_200_OK)
async def convert_html_to_json(html: str) -> dict:
    """
    Convert HTML document to json
    """
    output_json = html_to_json.convert(html)
    return {
        "success": True,
        "data": output_json
    }
