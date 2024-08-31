from fastapi import status

from httpx import AsyncClient, codes

client = AsyncClient()


async def image(response, query):
    request = await client.request(method="GET", url=f"https://lexica.art/api/v1/search?q={query}")
    if request.status_code != codes.OK:
        response.status_code = status.HTTP_200_OK
        return {
            "success": False,
            "data": None,
            "error_message": "A problem has occurred on our end"
        }

    return {
        "success": request.is_success,
        "data": request.json(),
        "error_message": None
    }
