from fastapi import APIRouter, Response, status

from typing import Optional

import httpx
import os

client = httpx.AsyncClient()

router = APIRouter(prefix="/api", tags=["Location"])


@router.get("/location", status_code=status.HTTP_200_OK)
@router.post("/location", status_code=status.HTTP_200_OK)
async def location(
        response: Response,
        text: str,
        latitude: Optional[float] = 0,
        longitude: Optional[float] = 0
) -> dict:
    """
    Search service for street names, places and old names (Search API)
    """
    access_key = os.getenv(key="NESHAN_KEY")

    url = "https://api.neshan.org/v1/"
    query_url = f"{url}search?term={text}&lat={latitude}&lng={longitude}"
    req = await client.request(
        method="POST", url=query_url, headers={
            "Api-Key": access_key
        }
    )
    if req.status_code != httpx.codes.OK:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "error_message": "A problem has occurred on our end"
        }

    return {
        "success": True,
        "data": req.json()
    }
