from fastapi import APIRouter, status
from fastapi.responses import FileResponse

import requests

router = APIRouter(prefix='/api', tags=['Anime'])


@router.get('/rand-anime', status_code=status.HTTP_200_OK)
@router.post('/rand-anime', status_code=status.HTTP_200_OK)
async def random_anime_image() -> "FileResponse":
    '''Get the icon from icon-icons.com'''
    request = requests.request(method='POST', url='https://pic.re/image')
    with open('app/tmpfiles/anime.png', 'wb+') as _file:
        _file.write(request.content)

    return FileResponse('app/tmpfiles/anime.png')
