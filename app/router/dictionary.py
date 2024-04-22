from fastapi import APIRouter, Response, status

import requests
import bs4

router = APIRouter(prefix='/api', tags=['Dictionary'])


@router.get('/dict/v1', status_code=status.HTTP_200_OK)
@router.post('/dict/v1', status_code=status.HTTP_200_OK)
async def dictionary(responce: Response, query: str) -> dict:
    '''Search words in deh khoda dictionary'''
    request = requests.request(
        method='GET', url=f'https://dehkhoda.ut.ac.ir/fa/dictionary/{query}'
    )
    if request.status_code != requests.codes.ok:
        responce.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'success': False, 'error_message': 'A problem has occurred on our end'
        }

    soup = bs4.BeautifulSoup(request.text, 'html.parser')
    paragraphs = soup.find('div', class_='definitions p-t-1')
    return {
        'success': True,
        'data': paragraphs.text
    }


@router.get('/dict/v2', status_code=status.HTTP_200_OK)
@router.post('/dict/v2', status_code=status.HTTP_200_OK)
async def dictionary(responce: Response, query: str) -> dict:
    '''Search words in Amid's Persian culture'''
    request = requests.request(
        method='GET', url=f'https://vajehyab.com/amid/{query}'
    )
    if request.status_code != requests.codes.ok:
        responce.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'success': False, 'error_message': 'A problem has occurred on our end'
        }

    soup = bs4.BeautifulSoup(request.text, 'html.parser')
    paragraphs = soup.find('div', class_='_51HBSo', role='definition')
    if paragraphs is None:
        return {
            'success': False,
            'error_message': 'Your word was not found in the dictionary'
        }

    return {
        'success': True,
        'data': paragraphs.text
    }
