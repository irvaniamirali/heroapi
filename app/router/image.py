from fastapi import APIRouter, Response, File, status
from fastapi.responses import FileResponse

from typing import Annotated
from PIL import Image


router = APIRouter(prefix='/api', tags=['Image'])

@router.get('/png2ico', status_code=status.HTTP_200_OK)
@router.post('/png2ico', status_code=status.HTTP_200_OK)
async def convert_image_to_ico_format(image: Annotated[bytes, File()]):
    '''Convert image in png format to ico'''
    FILE_PATH = 'app/tmpfiles/logo.png'
    with open(FILE_PATH, 'wb+') as _file:
        _file.write(image)

    logo = Image.open(FILE_PATH)
    ICO_FILE_PATH = re.sub('png', 'ico', FILE_PATH)
    logo.save(ICO_FILE_PATH, format='ico')
    return FileResponse(ICO_FILE_PATH)
