from fastapi import APIRouter, status

from app.api.sources.soundcloud import soundcloud

router = APIRouter(prefix="/api", tags=["Sound Cloud Downloader"])

@router.get("/soundcloud", status_code=status.HTTP_200_OK)
@router.post("/soundcloud", status_code=status.HTTP_200_OK)
async def sound_cloud(link_music: str):

    """
    this API for Download Track at https://soundcloud.com
    """

    return await soundcloud(link_music=link_music)
