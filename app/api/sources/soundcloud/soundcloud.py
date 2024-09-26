from sclib.asyncio import SoundcloudAPI

api = SoundcloudAPI()


async def track(url):
    track_result = await api.resolve(url)
    return track_result.to_dict()


async def playlist(url):
    playlist_result = await api.resolve(url)
    return playlist_result.to_dict()
