from fastapi import APIRouter, Response, status
from fastapi.responses import FileResponse

import segno
from random import randint

name_file = randint(0, 100000000000000000)

def generaqteQRcode(info_in_qrcode: str, scale: int, border: int):
    qrcode = segno.make_qr(info_in_qrcode)
    qrcode.save(
        f"{name_file}.png",
        scale=scale,
        border=border
    )

router = APIRouter(prefix='/api', tags=['QR Code'])

@router.get('/qrcode', status_code=status.HTTP_200_OK)
@router.post('/qrcode', status_code=status.HTTP_200_OK)
async def qrcode(text: str, scale: int = 10, border: int = 2) -> dict:
    'Convert Text to qrcode and Display qrcode in web'
    generaqteQRcode(text, scale, border)
    return FileResponse(f'{name_file}.png')