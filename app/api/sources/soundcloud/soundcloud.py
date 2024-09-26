from sclib.asyncio import SoundcloudAPI

api = SoundcloudAPI()


async def track(url):
    track_result = await api.resolve(url)

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


async def playlist(url):
    playlist_result = await api.resolve(url)

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
