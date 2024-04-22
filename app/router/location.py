from fastapi import APIRouter, Response, status

from typing import Optional
import requests
import os

router = APIRouter(prefix='/api', tags=['Location'])


@router.get('/location', status_code=status.HTTP_200_OK)
@router.post('/location', status_code=status.HTTP_200_OK)
async def location(
        responce: Response,
        text: str,
        latitude: Optional[float] = 0,
        longitude: Optional[float] = 0
) -> dict:
    '''Web service to get location and map'''
    access_key = os.getenv(key='NESHAN_KEY')
    query_url = f'https://api.neshan.org/v1/search?term={text}&lat={latitude}&lng={longitude}'
    request = requests.request(
        method='GET', url=query_url, headers={
            'Api-Key': access_key
        }
    )
    if request.status_code != requests.codes.ok:
        responce.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'success': False, 'error_message': 'A problem has occurred on our end'
        }

    return {
        'success': True,
        'data': request.json()
    }
