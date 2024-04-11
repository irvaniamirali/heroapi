from fastapi import APIRouter, status

from requests import request, codes
from typing import Optional

router = APIRouter(prefix='/api')

@router.get('/bardai', tags=['AI'], status_code=status.HTTP_200_OK)
@router.get('/bardai', tags=['AI'], status_code=status.HTTP_200_OK)
async def bard_ai(prompt: str):
    '''Bard artificial intelligence web service'''
    url = 'https://api.safone.dev/'
    prompt_request = request(method='GET', url=f'{url}bard?message={prompt}')
    if request.status_code != codes.ok:
        return {
            'success': False, 'error_message': 'A problem has occurred on our end'
        }

    responce = prompt_request.json()
    final_responce = responce['candidates'][0]['content']['parts'][0]['text']
    return {
        'success': True,
        'dev': 'Hero-Team',
        'url': 'https://t.me/HeroAPI',
        'github': 'https://github.com/metect/HeroAPI',
        'data': final_responce
    }
