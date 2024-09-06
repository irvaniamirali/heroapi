from fastapi import APIRouter, Response, status

from app.api.sources.soundcloud import track

router = APIRouter(prefix="/api", tags=["SoundCloud Downloader"])


@router.get("/soundcloud/track", status_code=status.HTTP_200_OK)
@router.post("/soundcloud/track", status_code=status.HTTP_200_OK)
async def soundcloud(response: Response, url: str) -> dict:
    """
    This API for Download Track at https://soundcloud.com
    """
    return await track(response, url)
