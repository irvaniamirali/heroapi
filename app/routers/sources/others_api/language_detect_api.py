from fastapi import APIRouter, Response, status

from app.api.sources.others_api import language_detect_api

router = APIRouter(prefix="/api")


@router.get("/lang", tags=["Language detect"], status_code=status.HTTP_200_OK)
@router.post("/lang", tags=["Language detect"], status_code=status.HTTP_200_OK)
async def language_detect(response: Response, text: str) -> dict:
    """
    Identifying the language of texts
    """
    return await language_detect_api(response, text)
