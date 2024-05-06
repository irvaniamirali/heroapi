from fastapi import APIRouter, Response, status

from g4f.client import Client
import requests

client = Client()

router = APIRouter(prefix='/api', tags=['AI'])


@router.get('/bard', status_code=status.HTTP_200_OK)
@router.post('/bard', status_code=status.HTTP_200_OK)
async def bard_ai(responce: Response, prompt: str) -> dict:
    '''Bard artificial intelligence web service'''
    url = 'https://api.safone.dev/'
    request = requests.request(method='POST', url=f'{url}bard?message={prompt}')
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


@router.get('/gpt', status_code=status.HTTP_200_OK)
@router.post('/gpt', status_code=status.HTTP_200_OK)
async def chatgpt_ai(responce: Response, prompt: str) -> dict:
    '''ChatGPT artificial intelligence web service'''
    message_data = {
        'role': 'user', 'content': prompt
    }
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[message_data],
    )
    return {
        'success': True,
        'data': response.choices[0].message.content
    }
