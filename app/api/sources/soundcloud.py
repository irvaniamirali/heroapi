from fastapi import status

from sclib.asyncio import SoundcloudAPI

from httpx import AsyncClient

client = AsyncClient()

api = SoundcloudAPI()


async def track(response, url):
    """
    SoundCloud Track Downloader
    """
    try:
        track_result = await api.resolve(url)
    except:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "data": None,
            "error_message": "A problem has occurred on our end"
        }

    stream_url = await track_result.get_stream_url()
    return {
        "artist": track_result.artist,
        "title": track_result.title,
        "artwork_url": track_result.artwork_url,
        "stream_url": stream_url,
        "comment_count": track_result.comment_count,
        "album": track_result.album,
        "license": track_result.license,
        "display_date": track_result.display_date,
        "download_count": track_result.download_count,
        "likes_count": track_result.likes_count,
        "public": track_result.public,
        "policy": track_result.policy,
        "release_date": track_result.release_date
    }
