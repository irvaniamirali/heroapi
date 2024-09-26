from fastapi import APIRouter, status

from app.api.sources.soundcloud import track, playlist

router = APIRouter(prefix="/api", tags=["SoundCloud Downloader"])


@router.get("/soundcloud/track", status_code=status.HTTP_200_OK)
async def soundcloud_track(url: str) -> dict:
    """
    This API for Fetch Track at https://soundcloud.com
    """
    return await track(url)


@router.get("/soundcloud/playlist", status_code=status.HTTP_200_OK)
async def soundcloud_playlist(url: str) -> dict:
    """
    This API for Fetch Playlist at https://soundcloud.com
    """
    return await playlist(url)
