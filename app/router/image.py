from fastapi import APIRouter, File, status
from fastapi.responses import FileResponse

from typing import Annotated

from bs4 import BeautifulSoup
from PIL import Image
import requests
import re

router = APIRouter(prefix='/api')


@router.get('/icon', tags=['Icon Search'], status_code=status.HTTP_200_OK)
@router.post('/icon', tags=['Icon Search'], status_code=status.HTTP_200_OK)
async def icon(responce: Response, query: str, page: Optional[int] = 1) -> dict:
    '''Get the icon from icon-icons.com'''
    request = requests.request(
        method='GET', url=f'https://icon-icons.com/search/icons/?filtro={query}&page={page}'
    )
    if request.status_code != requests.codes.ok:
        responce.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'success': False, 'error_message': 'A problem has occurred on our end'
        }

    soup = BeautifulSoup(request.text, 'html.parser')
    icons = soup.find_all('div', class_='icon-preview')

    search_result = list()
    for icon in icons:
        data_original = icon.find('img', class_='lazy', src=True)
        search_result.append(data_original.get('data-original'))

    return {
        'success': True,
        'data': search_result
    }


@router.get('/png2ico', tags=['Image'], status_code=status.HTTP_200_OK)
@router.post('/png2ico', tags=['Image'], status_code=status.HTTP_200_OK)
async def convert_image_to_ico_format(image: Annotated[bytes, File()]):
    '''Convert image in png format to ico'''
    FILE_PATH = 'app/tmpfiles/logo.png'
    with open(FILE_PATH, 'wb') as _file:
        _file.write(image)

    logo = Image.open(FILE_PATH)
    ICO_FILE_PATH = re.sub('png', 'ico', FILE_PATH)
    logo.save(ICO_FILE_PATH, format='ico')
    return FileResponse(ICO_FILE_PATH)
