from fastapi import APIRouter, Response, status
from fastapi.responses import FileResponse

# Import the following modules
from captcha.image import ImageCaptcha

router = APIRouter(prefix='/api', tags=['Captcha'])

@router.get('/captcha', status_code=status.HTTP_200_OK)
@router.post('captcha', status_code=status.HTTP_200_OK)
async def generateCaptcha(text: str, width: int = 280, height: int = 90):
    # Create an image instance of the given size
    image = ImageCaptcha(width = width, height = height)

    # Image captcha text
    captcha_text = text

    # generate the image of the given text
    data = image.generate(captcha_text) 

    # write the image on the given file and save it
    image.write(captcha_text, 'CAPTCHA.png')
    return FileResponse("CAPTCHA.png")