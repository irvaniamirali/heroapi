from fastapi import APIRouter, status
from fastapi.responses import FileResponse

from typing import Optional

from captcha.image import ImageCaptcha

router = APIRouter(prefix="/api", tags=["Captcha"])

FILE_PATH = "app/tmp/captcha.png"


@router.get("/captcha", status_code=status.HTTP_200_OK)
@router.post("captcha", status_code=status.HTTP_200_OK)
async def generate_captcha(text: str, width: Optional[int] = 280, height: Optional[int] = 90):
    """
    Generate captcha image
    """
    image = ImageCaptcha(width=width, height=height)
    image.write(text, FILE_PATH)
    return FileResponse(FILE_PATH)
