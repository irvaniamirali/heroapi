from fastapi import APIRouter, Response, status
from fastapi.responses import FileResponse

import segno

router = APIRouter(prefix='/api', tags=['QR Code'])

@router.get('/qrcode', status_code=status.HTTP_200_OK)
@router.post('/qrcode', status_code=status.HTTP_200_OK)
async def qrcode(text: str, scale: int = 10, border: int = 2):
    'Convert Text to qrcode and Display qrcode in web'
    qrcode = segno.make_qr(text)
    qrcode.save(
        "Image.png",
        scale=scale,
        border=border
    )
    return FileResponse('Image.png')