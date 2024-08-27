from fastapi import APIRouter, Response, status

from httpx import AsyncClient, codes

client = AsyncClient()

router = APIRouter(tags=["AI Image Generation"])


@router.get("/image", status_code=status.HTTP_200_OK)
@router.post("/image", status_code=status.HTTP_200_OK)
async def image(response: Response, query: str) -> dict:
    """
    Image Generator. [lexica](lexica.art)
    """
    request = await client.request(method="GET", url=f"https://lexica.art/api/v1/search?q={query}")
    if request.status_code != codes.OK:
        response.status_code = status.HTTP_200_OK
        return {
            "success": False,
            "data": None,
            "error_message": "A problem has occurred on our end"
        }

    return {
        "success": False,
        "data": request.json(),
        "error_message": None
    }
