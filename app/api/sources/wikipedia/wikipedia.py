from httpx import AsyncClient

client = AsyncClient()


async def search(query, lang, _format):
    """
    Do a Wikipedia search for `query`.
    """
    base_url = "https://%s.wikipedia.org/w/api.php?action=parse&page=%s&format=%s"
    response = await client.request(method="GET", url=base_url % (lang, query, _format))
    return response.json()
