from httpx import AsyncClient

from bs4 import BeautifulSoup

from re import findall

client = AsyncClient()


async def search(query, page):
    response = await client.request(method="GET", url=f"https://music-fa.com/search/{query}/page/{page}")
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article", class_="mf_pst")

    search_result = []
    for article in articles:
        title = article["data-artist"].strip()
        image_snippet = article.find("img", src=True)
        images = findall(
            r"https://music-fa\.com/wp-content/uploads/.*?\.jpg", str(image_snippet)
        )
        music = article.find("span", class_="play")
        try:
            link_for_download = music["data-song"]
        except TypeError:
            link_for_download = None

        search_result.append(
            dict(
                title=title,
                images=images,
                link_for_download=link_for_download
            )
        )

    return search_result
