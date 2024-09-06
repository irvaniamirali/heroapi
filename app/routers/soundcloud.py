from fastapi import APIRouter, Response, status

from app.api.sources.soundcloud import track, playlist

router = APIRouter(prefix="/api", tags=["SoundCloud Downloader"])


@router.get("/soundcloud/track", status_code=status.HTTP_200_OK)
@router.post("/soundcloud/track", status_code=status.HTTP_200_OK)
async def soundcloud_track(response: Response, url: str) -> dict:
    """
    This API for Fetch Track at https://soundcloud.com
    """
    return await track(response, url)


@router.get("/soundcloud/playlist", status_code=status.HTTP_200_OK)
@router.post("/soundcloud/playlist", status_code=status.HTTP_200_OK)
async def soundcloud_playlist(response: Response, url: str) -> dict:
    """
    This API for Fetch Playlist at https://soundcloud.com
    """
    return await playlist(response, url)
