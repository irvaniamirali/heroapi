from fastapi import APIRouter, Response, status

from requests import request, codes


router = APIRouter(prefix='/api', tags=['AI'])

@router.get('/bardai', status_code=status.HTTP_200_OK)
@router.post('/bardai', status_code=status.HTTP_200_OK)
async def bard_ai(responce: Response, prompt: str) -> dict:
    '''Bard artificial intelligence web service'''
    url = 'https://api.safone.dev/'
    prompt_request = request(method='GET', url=f'{url}bard?message={prompt}')
    if request.status_code != codes.ok:
        responce.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'success': False, 'error_message': 'A problem has occurred on our end'
        }

    responce = prompt_request.json()
    final_responce = responce['candidates'][0]['content']['parts'][0]['text']
    return {
        'success': True,
        'data': final_responce
    }
