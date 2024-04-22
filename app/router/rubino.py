from fastapi import APIRouter, Response, status

from typing import Optional
import requests
import random

router = APIRouter(prefix='/api', tags=['Social media'])


@router.get('/rubino', status_code=status.HTTP_200_OK)
@router.post('/rubino', status_code=status.HTTP_200_OK)
async def rubino(responce: Response, auth: str, url: str, timeout: Optional[float] = 10) -> dict:
    '''This api is used to get the information of the post(s) in Rubino Messenger'''
    payload: dict = {
        'api_version': '0',
        'auth': auth,
        'client': {
            'app_name': 'Main',
            'app_version': '3.0.1',
            'package': 'app.rubino.main',
            'lang_code': 'en',
            'platform': 'PWA'
        },
        'data': {
            'share_link': url.split('/')[-1],
            'profile_id': None
        },
        'method': 'getPostByShareLink'
    }
    url = f'https://rubino{random.randint(1, 20)}.iranlms.ir/'
    request = requests.request(method='GET', url=url, timeout=timeout, json=payload)
    if request.status_code != requests.codes.ok:
        responce.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'success': False, 'error_message': 'A problem has occurred on our end'
        }

    return {
        'success': True,
        'data': request.json()
    }
