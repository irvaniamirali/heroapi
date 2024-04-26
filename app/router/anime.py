from fastapi import APIRouter, Response, status
from fastapi.responses import FileResponse

import requests

router = APIRouter(prefix='/api', tags=['Anime'])


@router.get('/rand-anime', status_code=status.HTTP_200_OK)
@router.post('/rand-anime', status_code=status.HTTP_200_OK)
async def random_anime_image(responce: Response) -> "FileResponse":
    '''Get the icon from icon-icons.com'''
    request = requests.request(method='POST', url='https://pic.re/image')
    if request.status_code != requests.codes.ok:
        responce.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'success': False,
            'error_message': 'A problem has occurred on our end'
        }

    with open('app/tmpfiles/anime.png', 'wb+') as _file:
        _file.write(request.content)

    return FileResponse('app/tmpfiles/anime.png')
