from fastapi import APIRouter, status

from app.api.sources.ai import lexica_api

router = APIRouter(prefix="/api", tags=["AI", "Image Generator"])


@router.get("/lexica", status_code=status.HTTP_200_OK)
async def lexica(query: str) -> dict:
    """
    AI Image Generator. [lexica](https://lexica.art)
    """
    return await lexica_api(query)
