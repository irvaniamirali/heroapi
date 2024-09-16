from fastapi import status

from sclib.asyncio import SoundcloudAPI

api = SoundcloudAPI()


async def track(response, url):
    try:
        track_result = await api.resolve(url)
    except:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error_message": "A problem has occurred on our end."}

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


async def playlist(response, url):
    try:
        playlist_result = await api.resolve(url)
    except:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error_message": "A problem has occurred on our end."}

    results = []
    for _track in playlist_result.tracks:
        stream_url = await _track.get_stream_url()
        results.append(
            {
                "artist": _track.artist,
                "title": _track.title,
                "artwork_url": _track.artwork_url,
                "stream_url": stream_url,
                "comment_count": _track.comment_count,
                "album": _track.album,
                "license": _track.license,
                "display_date": _track.display_date,
                "download_count": _track.download_count,
                "likes_count": _track.likes_count,
                "public": _track.public,
                "policy": _track.policy,
                "release_date": _track.release_date
            }
        )

    return results
