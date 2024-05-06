from fastapi import APIRouter, Response, status

from typing import Optional
from faker import Faker

router = APIRouter(prefix='/api', tags=['Fake data'])


@router.get('/ftext', status_code=status.HTTP_200_OK)
@router.post('/ftext', status_code=status.HTTP_200_OK)
async def fake_text(responce: Response, _len: Optional[int] = 99, lang: Optional[str] = 'en') -> dict:
    if int(_len) > 1000:
        responce.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'success': False, 'error_message': 'The amount is too big. Send a smaller number `_len`'
        }

    return {
        'success': True,
        'data': Faker([lang]).text(_len)
    }


@router.get('/femail', status_code=status.HTTP_200_OK)
@router.post('/femail', status_code=status.HTTP_200_OK)
async def fake_email(responce: Response, count: Optional[int] = 99) -> dict:
    if int(count) > 100:
        responce.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'success': False, 'error_message': 'The amount is too big. Send a smaller number `count`'
        }

    final_values = list()
    for _ in range(count):
        final_values.append(Faker().email())

    return {
        'success': True,
        'data': final_values
    }


@router.get('/fname', status_code=status.HTTP_200_OK)
@router.post('/fname', status_code=status.HTTP_200_OK)
async def fake_name(responce: Response, count: Optional[int] = 99, lang: Optional[str] = 'en') -> dict:
    if int(count) > 100:
        responce.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'success': False, 'error_message': 'The amount is too big. Send a smaller number `count`'
        }

    final_values = list()
    for _ in range(count):
        final_values.append(Faker([lang]).name())

    return {
        'success': True,
        'data': final_values
    }
