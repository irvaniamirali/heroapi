from sclib import SoundcloudAPI, Track
from fastapi.responses import  FileResponse

async def soundcloud(link_music):

    api = SoundcloudAPI()
    track = api.resolve(link_music)

    assert type(track) is Track

    filename = f'./{track.artist} - {track.title}.mp3'
    return FileResponse(filename)
