from bs4 import BeautifulSoup

from httpx import AsyncClient

client = AsyncClient()

BASE_URL = "https://icon-icons.com"


async def icon_search(query, page):
    request = await client.request("GET", url=f"{BASE_URL}/search/icons/?filtro={query}&page={page}")
    soup = BeautifulSoup(request.text, "html.parser")
    icons = soup.find_all("div", class_="icon-preview")

    search_results = []
    for icon in icons:
        data_original = icon.find("img", loading="lazy", src=True)
        search_results.append(data_original.get("src"))

    return {
        "success": True,
        "data": search_results,
        "error_message": None
    }
