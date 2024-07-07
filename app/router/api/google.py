from fastapi import APIRouter, status

from typing import Optional
from bs4 import BeautifulSoup

import user_agent
import requests

router = APIRouter(prefix="/api", tags=["Google search"])


def request(query, results, lang, start, safe, ssl_verify):
    response = requests.request(
        method="GET",
        url="https://www.google.com/search",
        headers={
            "User-Agent": user_agent.generate_user_agent()
        },
        params={
            "q": query,
            "num": results + 2,
            "hl": lang,
            "start": start,
            "safe": safe,
        },
        verify=ssl_verify,
    )
    return response


def search(query, num_results, lang, safe, ssl_verify=None):
    escaped_term = query.replace(" ", "+")
    start = 0
    fetched_results = 0

    results = list()
    while fetched_results < num_results:

        response = request(escaped_term, num_results - start, lang, start, safe, ssl_verify)
        soup = BeautifulSoup(response.text, "html.parser")
        result_block = soup.find_all("div", attrs={"class": "g"})
        new_results = 0

        for result in result_block:
            link = result.find("a", href=True)
            title = result.find("h3").text
            description_box = result.find("div", {"style": "-webkit-line-clamp:2"})

            if link and title and description_box:
                fetched_results += 1
                new_results += 1
                results.append(
                    {
                        "link": link["href"],
                        "title": title,
                        "description": description_box.text
                    }
                )

            if fetched_results >= num_results:
                break

        if new_results == 0:
            break

        start += 10

        return results


@router.get("/google", status_code=status.HTTP_200_OK)
@router.post("/google", status_code=status.HTTP_200_OK)
async def google_search(
        query: str,
        num_results: Optional[int] = 10,
        lang: Optional[str] = "en",
        safe: Optional[str] = "active",
) -> dict:
    """
    Search the Google search engine
    """
    results = search(query=query, num_results=num_results, lang=lang, safe=safe)
    while results is None:
        results = search(query=query, num_results=num_results, lang=lang, safe=safe)

    return {
        "success": True,
        "data": results
    }
