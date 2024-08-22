from fastapi import APIRouter, status
from fastapi.responses import FileResponse

from sclib import SoundcloudAPI, Track


router = APIRouter(tags=["SoundCloud Downloader"])


@router.get("/soundCloud", status_code=status.HTTP_200_OK)
@router.post("/soundCloud", status_code=status.HTTP_200_OK)
async def SoundCloud(url: str):
    api = SoundcloudAPI()
    track = api.resolve(url)

    assert type(track) is Track

    filename = f'./{track.artist} - {track.title}.mp3'
    return FileResponse(filename)
