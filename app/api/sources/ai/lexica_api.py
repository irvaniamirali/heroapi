from httpx import AsyncClient, codes

client = AsyncClient()

HOST = "https://lexica.art/api/v1/search?q={}"


async def lexica_api(query):
    """
    Generate Image AI
    """
    response = await client.request(method="GET", url=HOST.format(query))
    response.raise_for_status()
    return response.json()
