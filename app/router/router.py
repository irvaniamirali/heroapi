from fastapi import APIRouter, Request, File, HTTPException, status
from fastapi.responses import FileResponse

from typing import Annotated, Optional

import os
import requests
import urllib.parse
import re
import html
import langdetect
import json
import random
import faker
import bs4
import base64
import codecs
from PIL import Image

router = APIRouter(prefix='/api')


@router.get('/music-fa', tags=['Music search'], status_code=status.HTTP_200_OK)
@router.post('/music-fa', tags=['Music search'], status_code=status.HTTP_200_OK)
async def music_fa(query: str, page: Optional[int] = 1):
    '''Search and search web service on the [music-fa](https://music-fa.com) site'''




@router.get('/rubino', tags=['Social media'], status_code=status.HTTP_200_OK)
@router.post('/rubino', tags=['Social media'], status_code=status.HTTP_200_OK)
async def rubino(auth: str, url: str, timeout: Optional[float] = 10):
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
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='A problem has occurred on our end'
        )

    return execute(success=True, data=request.json())


@router.get('/translate', tags=['Translate'], status_code=status.HTTP_200_OK)
@router.post('/translate', tags=['Translate'], status_code=status.HTTP_200_OK)
async def translate(text: str, to_lang: Optional[str] = 'auto', from_lang: Optional[str] = 'auto'):
    '''Translation of texts based on the Google Translate engine'''
    url = 'https://translate.google.com'
    final_url = f'{url}/m?tl={to_lang}&sl={from_lang}&q={urllib.parse.quote(text)}'
    request = requests.request(
        method='GET', url=final_url, headers={
            'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0'
        }
    )
    if request.status_code != requests.codes.ok:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='A problem has occurred on our end'
        )

    result = re.findall(r'(?s)class="(?:t0|result-container)">(.*?)<', request.text)
    return execute(success=True, data=html.unescape(result[0]))


@router.get('/github-topic-search', tags=['Github'], status_code=status.HTTP_200_OK)
@router.post('/github-topic-search', tags=['Github'], status_code=status.HTTP_200_OK)
async def github_topic_search(query: str, per_page: Optional[int] = 30, page: Optional[int] = 1):
    '''Github topic search web service'''
    headers = {
        'Accept': 'application/vnd.github+json'
    }
    url = 'https://api.github.com/search/topics?q=%s&per_page=%s&page=%s'
    request = requests.request(method='GET', url=url % (query, per_page, page), headers=headers)
    if request.status_code != requests.codes.ok:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='A problem has occurred on our end'
        )

    return execute(success=True, data=request.json())


@router.get('/github-repo-search', tags=['Github'], status_code=status.HTTP_200_OK)
@router.post('/github-repo-search', tags=['Github'], status_code=status.HTTP_200_OK)
async def github_repo_search(
        name: str,
        sort: Optional[str] = 'stars',
        order: Optional[str] = 'desc',
        per_page: Optional[int] = 30,
        page: Optional[int] = 1
):
    '''Github repository search web service.
    sortlist repository: "stars", "forks", "help-wanted-issues", "updated"
    '''
    headers = {
        'Accept': 'application/vnd.github+json'
    }
    url = 'https://api.github.com/search/repositories?q=%s&s=%s&order=%s&per_page=%s&page=%s'
    request = requests.request(
        method='GET', url=url % (name, sort, order, per_page, page), headers=headers
    )
    if request.status_code != requests.codes.ok:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='A problem has occurred on our end'
        )

    return execute(success=True, data=request.json())


@router.get('/github-users-search', tags=['Github'], status_code=status.HTTP_200_OK)
@router.post('/github-users-search', tags=['Github'], status_code=status.HTTP_200_OK)
async def github_users_search(
        query: str,
        sort: Optional[str] = 'followers',
        order: Optional[str] = 'desc',
        per_page: Optional[int] = 30,
        page: Optional[int] = 1,
):
    '''Github users search web service.
    sortlist repository: "followers", "repositories", "joined"
    '''
    headers = {
        'Accept': 'application/vnd.github+json'
    }
    url = 'https://api.github.com/search/users?q=%s&sort=%s&order=%s&per_page=%s&page=%s'
    request = requests.request(
        method='GET', url=url % (query, sort, order, per_page, page), headers=headers
    )
    if request.status_code != requests.codes.ok:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='A problem has occurred on our end'
        )

    return execute(success=True, data=request.json())


@router.get('/pypi', tags=['PyPi'], status_code=status.HTTP_200_OK)
@router.post('/pypi', tags=['PyPi'], status_code=status.HTTP_200_OK)
async def pypi_package_search(query: str):
    '''PyPi package search web service'''
    query = '+'.join(query.split())
    request = requests.request(method='GET', url=f'https://pypi.org/search/?q={query}')
    if request.status_code != requests.codes.ok:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='A problem has occurred on our end'
        )

    soup = bs4.BeautifulSoup(request.text, 'html.parser')
    package_snippets = soup.find_all('a', class_='package-snippet')

    search_results = list()
    for package_snippet in package_snippets:
        span_elems = package_snippet.find_all('span')
        name = span_elems[0].text.strip()
        version = span_elems[1].text.strip()
        release_date = span_elems[2].text.strip()
        description = package_snippet.p.text.strip()
        search_results.append(
            dict(
                name=name,
                version=version,
                release_date=release_date,
                description=description
            )
        )

    return execute(success=True, data=search_results)


@router.get('/icon', tags=['Icon'], status_code=status.HTTP_200_OK)
@router.post('/icon', tags=['Icon'], status_code=status.HTTP_200_OK)
async def icon(query: str, page: Optional[int] = 1):
    '''Get the icon from icon-icons.com'''
    request = requests.request(method='GET', url=f'https://icon-icons.com/search/icons/?filtro={query}')
    if request.status_code != requests.codes.ok:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='A problem has occurred on our end'
        )

    soup = bs4.BeautifulSoup(request.text, 'html.parser')
    icons = soup.find_all('div', class_='icon-preview')

    search_result = list()
    for icon in icons:
        data_original = icon.find('img', class_='lazy', src=True)
        search_result.append(data_original['data-original'])

    return execute(success=True, data=search_result)


@router.get('/rand-anime', tags=['Anime'], status_code=status.HTTP_200_OK)
@router.post('/rand-anime', tags=['Anime'], status_code=status.HTTP_200_OK)
async def random_anime():
    '''return random 4K anime picture'''
    request = requests.request(method='GET', url='https://pic.re/image')
    if request.status_code != requests.codes.ok:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='A problem has occurred on our end'
        )

    with open('app/tmpfiles/anime.png', 'wb+') as _file:
        _file.write(request.content)

    return FileResponse('app/tmpfiles/anime.png')


@router.get('/domain-price', tags=['Domain'], status_code=status.HTTP_200_OK)
@router.post('/domain-price', tags=['Domain'], status_code=status.HTTP_200_OK)
async def domain_price():
    '''Get Domain price from [parsvds.com](https://parsvds.com) web site'''
    request = requests.request(method='GET', url=f'https://parsvds.com/domain/')
    if request.status_code != requests.codes.ok:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='A problem has occurred on our end'
        )

    soup = bs4.BeautifulSoup(request.text, 'html.parser')
    table_rows = soup.find_all('tr')

    search_result = list()
    for row in table_rows[1:]:
        domain = row.find_all('td')
        price = row.find_all('td')
        search_result.append(
            dict(
                domain=domain[0].text, price=price[1].text
            )
        )

    return execute(success=True, data=search_result)


@router.get('/bs64encode', tags=['Base64'], status_code=status.HTTP_200_OK)
@router.post('/bs64encode', tags=['Base64'], status_code=status.HTTP_200_OK)
async def b64(text : str) -> dict:
    b_string = codecs.encode(text, 'utf-8')
    output = base64.b64encode(b_string)
    return execute(success=True, data=output)


@router.get('/bs64decode', tags=['Base64'], status_code=status.HTTP_200_OK)
@router.post('/bs64decode', tags=['Base64'], status_code=status.HTTP_200_OK)
async def b64encode(text : str) -> dict:
    b_string = codecs.encode(text, 'utf-8')
    try:
        output = base64.b64decode(b_string)
        return execute(success=True, data=output)
    except:
        return execute(success=False, data='This Text Not Base64')


@router.get('/png2ico', tags=['Image'], status_code=status.HTTP_200_OK)
@router.post('/png2ico', tags=['Image'], status_code=status.HTTP_200_OK)
async def convert_image_to_ico_format(image: Annotated[bytes, File()]):
    '''Convert image in png format to ico'''
    FILE_PATH = 'app/tmpfiles/logo.png'
    with open(FILE_PATH, 'wb+') as _file:
        _file.write(image)

    logo = Image.open(FILE_PATH)
    ICO_FILE_PATH = re.sub('png', 'ico', FILE_PATH)
    logo.save(ICO_FILE_PATH, format='ico')
    return FileResponse(ICO_FILE_PATH)
