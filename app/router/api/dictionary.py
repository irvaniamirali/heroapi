from fastapi import APIRouter, Response, status

import requests
import bs4
import re

router = APIRouter(prefix='/api', tags=['Dictionary'])


@router.get('/dict/v1', status_code=status.HTTP_200_OK)
@router.post('/dict/v1', status_code=status.HTTP_200_OK)
async def dictionary(query: str) -> dict:
    '''Search words in deh khoda dictionary'''
    request = requests.request(
        method='GET', url=f'https://dehkhoda.ut.ac.ir/fa/dictionary/{query}'
    )
    soup = bs4.BeautifulSoup(request.text, 'html.parser')
    paragraphs = soup.find('div', class_='definitions p-t-1')

    if not paragraphs:
        return {
            'success': False,
            'error': 'Your word was not found in the dictionary'
        }

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
    soup = bs4.BeautifulSoup(request.text, 'html.parser')
    paragraph_tag = soup.find('div', class_='_51HBSo', role='definition')
    if paragraph_tag is None:
        responce.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'success': False,
            'error_message': 'Your word was not found in the dictionary'
        }

    paragraphs = re.findall(
        r'^<div\ class=\".*\"\ role=\"definition\">(.*?)</div>$', str(paragraph_tag)
    )
    clean_paragraphs = paragraphs[0].split('<br/>')
    return {
        'success': True,
        'data': clean_paragraphs
    }
