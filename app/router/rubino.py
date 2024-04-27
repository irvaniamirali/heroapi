from fastapi import APIRouter, Response, status

from typing import Optional
import requests
import random

router = APIRouter(prefix='/api', tags=['Social media'])


@router.get('/rubino', status_code=status.HTTP_200_OK)
@router.post('/rubino', status_code=status.HTTP_200_OK)
async def rubino(responce: Response, auth: str, url: str, timeout: Optional[float] = 10) -> dict:
    '''This api is used to get the information of the post(s) in Rubino Messenger'''
    payload = {
        "auth": "fylyhbfkrjspyqesrinhwdcpzwuwlisq",
        "api_version": "0",
        "client": {
            "app_name": "Main",
            "app_version": "2.1.6",
            "package": "m.rubika.ir",
            "platform": "PWA"
        },
        "data": {
            "profile_id": "660fe1763b775019c3cb3b32",
            "post_id": "6621ea973b77505229938ffb",
            "post_profile_id": "65e439253b775060f72e1509",
            "start_id": None,
            "limit": 5
        },
        "method": "getRelatedExplorePost"
    }
    url = f'https://rubino{random.randint(1, 20)}.iranlms.ir/'
    request = requests.request(
        method='POST', url=url, timeout=timeout, json=payload, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Accept': 'application/json, text/plain, */*'
        }
    )
    # if request.status_code != requests.codes.ok:
    #     responce.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    #     return {
    #         'success': False, 'error_message': 'A problem has occurred on our end'
    #     }

    return {
        'success': False,
        'data': 'This web service is currently unavailable'
    }
