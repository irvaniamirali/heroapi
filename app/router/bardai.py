from fastapi import APIRouter, Response, status

import requests

router = APIRouter(prefix='/api', tags=['AI'])


@router.get('/bard', status_code=status.HTTP_200_OK)
@router.post('/bard', status_code=status.HTTP_200_OK)
async def bard_ai(responce: Response, prompt: str) -> dict:
    '''Bard artificial intelligence web service'''
    url = 'https://api.safone.dev/'
    request = requests.request(method='GET', url=f'{url}bard?message={prompt}')
    if request.status_code != requests.codes.ok:
        responce.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'success': False, 'error_message': 'A problem has occurred on our end'
        }

    responce = request.json()
    return {
        'success': True,
        'data': responce
    }
