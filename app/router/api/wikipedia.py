from fastapi import APIRouter, Response, status

from typing import Optional

from httpx import AsyncClient, codes

client = AsyncClient()

router = APIRouter(prefix="/wikipedia", tags=["Wikipedia Search"])


@router.get("/search", status_code=status.HTTP_200_OK)
@router.post("/search", status_code=status.HTTP_200_OK)
async def wikipedia_search(
        response: Response,
        query: str,
        lang: Optional[str] = "en",
        format: Optional[str] = "json"
):
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
