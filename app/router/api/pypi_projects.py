from httpx import AsyncClient

from bs4 import BeautifulSoup

client = AsyncClient()


async def pypi_package_search(name):
    """
    PyPi package search web service
    """
    query = "+".join(name.split())
    request = await client.request("GET", url=f"https://pypi.org/search/?q={query}")
    soup = BeautifulSoup(request.text, "html.parser")
    package_snippets = soup.find_all("a", class_="package-snippet")

    search_results = []
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
        "data": search_results,
        "error_message": None
    }
