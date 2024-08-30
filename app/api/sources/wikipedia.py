from fastapi import status

from httpx import AsyncClient, codes

client = AsyncClient()


async def search(response, query, lang, format):
    """
    Do a Wikipedia search for `query`.
    """
    base_url = "https://%s.wikipedia.org/w/api.php?action=parse&page=%s&format=%s"
    request = await client.request(method="GET", url=base_url % (lang, query, format))
    if request.status_code != codes.OK:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "data": None,
            "error_message": "A problem has occurred on our end"
        }

    return {
        "success": True,
        "data": request.json(),
        "error_message": False
    }
