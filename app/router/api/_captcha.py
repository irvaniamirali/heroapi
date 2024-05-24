from fastapi import APIRouter, status
from fastapi.responses import FileResponse

from typing import Optional

from captcha.image import ImageCaptcha

router = APIRouter(prefix='/api', tags=['Captcha'])


@router.get('/captcha', status_code=status.HTTP_200_OK)
@router.post('captcha', status_code=status.HTTP_200_OK)
async def generateCaptcha(text: str, width: Optional[int] = 280, height: Optional[int] = 90):
    image = ImageCaptcha(width = width, height = height)
    data = image.generate(text)
    image.write(text, 'CAPTCHA.png')
    return FileResponse("CAPTCHA.png")
