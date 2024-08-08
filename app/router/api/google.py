from fastapi import APIRouter, status

from typing import Optional

import httpx
import user_agent

from bs4 import BeautifulSoup

client = httpx.AsyncClient()

router = APIRouter(prefix="/google", tags=["Google Search"])


async def request(term, results, lang, start, timeout, region):
    """
    Execute asynchronous request
    """
    params = {
        "q": term,
        "num": results + 2,
        "hl": lang,
        "start": start,
        "safe": "active",
        "gl": region,
    }
    response = await client.request(
        method="GET",
        url="https://www.google.com/search",
        headers={
            "User-Agent": user_agent.generate_user_agent()
        },
        params=params,
        timeout=timeout,
    )
    return response


@router.get("/search", status_code=status.HTTP_200_OK)
@router.post("/search", status_code=status.HTTP_200_OK)
async def google_search(
        query: str,
        lang: Optional[str] = "en",
        num_results: Optional[int] = 10,
        timeout: Optional[int] = 10,
        region: Optional[str] = ""
):
    """
    Search the Google search engine
    """
    results = []
    start = 0
    fetched_results = 0

    while fetched_results < num_results:
        response = await request(query, num_results - start, lang, start, timeout, region)
        soup = BeautifulSoup(response.text, "html.parser")
        result_block = soup.find_all("div", _class="g")
        new_results = 0

        for result in result_block:
            link = result.find("a", href=True)
            title = result.find("h3")
            description_box = result.find(
                "div", {
                    "style": "-webkit-line-clamp:2"
                }
            )

            if link and title and description_box:
                description = description_box.text
                fetched_results += 1
                new_results += 1
                results.append(
                    {
                        "link": link["href"],
                        "title": title.text,
                        "description": description
                    }
                )

            if fetched_results >= num_results:
                break

        if new_results == 0:
            break

        start += 10

    return {
        "success": True,
        "data": results,
        "error_message": None
    }
