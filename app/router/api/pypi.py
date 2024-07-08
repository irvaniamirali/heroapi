from fastapi import APIRouter, Response, status

from bs4 import BeautifulSoup

import httpx

client = httpx.AsyncClient()

router = APIRouter(prefix="/api", tags=["PyPi"])


@router.get("/pypi", status_code=status.HTTP_200_OK)
@router.post("/pypi", status_code=status.HTTP_200_OK)
async def pypi_package_search(response: Response, query: str) -> dict:
    """
    PyPi package search web service
    """
    query = "+".join(query.split())
    req = await client.request(method="GET", url=f"https://pypi.org/search/?q={query}")
    if req.status_code != httpx.codes.OK:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "error_message": "A problem has occurred on our end"
        }

    soup = BeautifulSoup(req.text, "html.parser")
    package_snippets = soup.find_all("a", class_="package-snippet")

    search_results = list()
    for package_snippet in package_snippets:
        span_elems = package_snippet.find_all("span")
        name = span_elems[0].text.strip()
        version = span_elems[1].text.strip()
        release_date = span_elems[2].text.strip()
        description = package_snippet.p.text.strip()
        search_results.append(
            dict(
                name=name,
                version=version,
                release_date=release_date,
                description=description
            )
        )

    return {
        "success": True,
        "data": search_results
    }
