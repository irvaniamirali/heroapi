from fastapi import APIRouter, Response, status

from app.api.sources.ai.lexica_api import image

router = APIRouter(prefix="/api", tags=["AI", "Image Generator"])


@router.get("/lexica", status_code=status.HTTP_200_OK)
@router.post("/lexica", status_code=status.HTTP_200_OK)
async def lexica(response: Response, query: str) -> dict:
    """
    AI Image Generator. [lexica](lexica.art)
    """
    return await image(response, query)
