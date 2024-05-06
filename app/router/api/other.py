from fastapi import APIRouter, Response, File, status
from fastapi.responses import FileResponse

from bs4 import BeautifulSoup
from PIL import Image
import requests
import re

import pyttsx3

import langdetect

from typing import Optional, Annotated

engine = pyttsx3.init()

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


@router.get('/text2voice', tags=['Text to voice'], status_code=status.HTTP_200_OK)
@router.post('/text2voice', tags=['Text to voice'], status_code=status.HTTP_200_OK)
async def text_to_voice(text: str) -> "FileResponse":
    '''Convert text to voice (without artificial intelligence)'''
    FILE_PATH = '/tmp/.heroapi/speech.mp3'
    engine.save_to_file(text=text, filename=FILE_PATH)
    engine.runAndWait()
    return FileResponse(FILE_PATH)


@router.get('/lang', tags=['Language Detect'], status_code=status.HTTP_200_OK)
@router.post('/lang', tags=['Language Detect'], status_code=status.HTTP_200_OK)
async def language_detect(responce: Response, text: str) -> dict:
    '''Identifying the language of texts'''
    try:
        result_detected = langdetect.detect(text)
        return {
            'success': True,
            'data': result_detected
        }
    except langdetect.LangDetectException:
        responce.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'success': False,
            'error_message': 'The value of the `text` parameter is not invalid'
        }
