from fastapi import APIRouter, Response, status

from typing import Optional

import httpx
import os

client = httpx.AsyncClient()

router = APIRouter(tags=["Location"])

access_key = os.getenv(key="NESHAN_KEY")

headers: dict = {
    "Api-Key": access_key
}


async def create_request(path: str, headers: dict):
    """
    Make asynchronous request to Neshan API
    """
    response = await client.request(method="GET", url=path, headers=headers)
    return response


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
    path = "https://api.neshan.org/v1/search?term=%s&lat=%s&lng=%s" % (text, latitude, longitude)
    request = await create_request(path=path, headers=headers)
    if request.status_code != httpx.codes.OK:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "data": None,
            "error_message": "A problem has occurred on our end"
        }

    return {
        "success": True,
        "data": request.json(),
        "error_message": None
    }
