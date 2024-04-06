from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import FileResponse

import os
import requests
import jalali.Jalalian
import urllib.parse
import re
import html
import langdetect
import json
import random
import faker
import bs4
import jdatetime
import base64
import codecs

router = APIRouter(prefix='/api')

def execute(success: bool = True, data: dict = None, err_message: str = None) -> dict:
    return dict(
        success=success,
        dev='Hero-Team',
        url='https://t.me/HeroAPI',
        github='https://github.com/Hero-API/HeroAPI',
        data=data,
    )


@router.get('/bard', tags=['AI'], status_code=status.HTTP_200_OK)
@router.post('/bard', tags=['AI'], status_code=status.HTTP_200_OK)
async def bard_ai(prompt: str):
    '''Bard artificial intelligence web service'''
    url = 'https://api.safone.dev/'
    request = requests.request(method='GET', url=f'{url}bard?message={prompt}')
    if request.status_code != requests.codes.ok:
        return await execute(success=False, err_message='A problem has occurred on our end')

    responce = request.json()
    final_responce = responce['candidates'][0]['content']['parts'][0]['text']
    return execute(success=True, data=final_responce)



@router.get('/font', tags=['Art'], status_code=status.HTTP_200_OK)
@router.post('/font', tags=['Art'], status_code=status.HTTP_200_OK)
async def font(text: str):
    '''Generate ascii fonts. Currently only English language is supported'''
    if langdetect.detect(text) in ['fa', 'ar', 'ur']:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Currently, Persian language is not supported'
        )
    else:
        with open('app/jsonfiles/font.json', 'r') as f:
            fonts = json.load(f)

        converted_text = str()
        for count in range(0, len(fonts)):
            for char in text:
                if char.isalpha():
                    char_index = ord(char.lower()) - 97
                    converted_text += fonts[str(count)][char_index]
                else:
                    converted_text += char

            converted_text += '\n'
            final_values = converted_text.split('\n')[0:-1]

        return execute(success=True, data=final_values)


@router.get('/datetime', tags=['Date & time'], status_code=status.HTTP_200_OK)
@router.post('/datetime', tags=['Date & time'], status_code=status.HTTP_200_OK)
async def datetime(tr_num: str = 'en'):
    '''Display detailed information about the date of the solar calendar'''
    current_date = jalali.Jalalian.jdate('H:i:s ,Y/n/j', tr_num=tr_num)
    return execute(success=True, data=current_date)


@router.get('/convert-date', tags=['Date & time'], status_code=status.HTTP_200_OK)
@router.post('/convert-date', tags=['Date & time'], status_code=status.HTTP_200_OK)
async def convert_date(day: int, month: int, year: int):
    '''Convert Shamsi date to Gregorian'''
    result_date = jdatetime.date(day=day, month=month, year=year).togregorian()
    return execute(success=True, data=result_date)


@router.get('/faker', tags=['Fake data'], status_code=status.HTTP_200_OK)
@router.post('/faker', tags=['Fake data'], status_code=status.HTTP_200_OK)
async def fake_data(item: str, count: int = 100, lang: str = 'en'):
    '''Production fake data. items: (`text`, `name`, `email`)'''
    if count > 100:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The amount is too big. Send a smaller number `count`'
        )
    else:
        final_values = list()
        if item == 'text':
            return execute(success=True, data=faker.Faker([lang]).text(count))
        elif item == 'name':
            for i in range(count):
                final_values.append(faker.Faker([lang]).name())

        elif item == 'email':
            for i in range(count):
                final_values.append(faker.Faker([lang]).email())

    return execute(success=True, data=final_values)


@router.get('/lang', tags=['Identify language'], status_code=status.HTTP_200_OK)
@router.post('/lang', tags=['Identify language'], status_code=status.HTTP_200_OK)
async def language_detect(text: str):
    '''Identifying the language of texts'''
    try:
        result_detected = langdetect.detect(text)
        return execute(success=True, data=result_detected)
    except langdetect.LangDetectException:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The value of the `text` parameter is not invalid'
        )


@router.get('/location', tags=['Location'], status_code=status.HTTP_200_OK)
@router.post('/location', tags=['Location'], status_code=status.HTTP_200_OK)
async def location(text: str, latitude: float, longitude: float):
    '''Web service to get location and map'''
    access_key = os.getenv(key='NESHAN_KEY')
    url = f'https://api.neshan.org/v1/search?term={text}&lat={latitude}&lng={longitude}'
    request = requests.request(
        method='GET', url=url, headers={
            'Api-Key': access_key
        }
    )
    if request.status_code != requests.codes.ok:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='A problem has occurred on our end'
        )

    return execute(success=True, data=request.json())


@router.get('/music-fa', tags=['Music search'], status_code=status.HTTP_200_OK)
@router.post('/music-fa', tags=['Music search'], status_code=status.HTTP_200_OK)
async def music_fa(query: str, page: int = 1):
    '''Search and search web service on the [music-fa](https://music-fa.com) site'''
    request = requests.request('GET', f'https://music-fa.com/search/{query}/page/{page}')
    if request.status_code != requests.codes.ok:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='A problem has occurred on our end'
        )

    soup = bs4.BeautifulSoup(request.text, 'html.parser')
    articles = soup.find_all('article', class_='mf_pst')

    search_result = list()
    for article in articles:
        title = article['data-artist'].strip()
        image_snippet = article.find('img', src=True)
        images = re.findall(
            r'https://music-fa\.com/wp-content/uploads/.*?\.jpg', str(image_snippet)
        )
        music = article.find('span', class_='play')
        link_for_download = music['data-song']
        search_result.append(
            dict(
                title=title,
                images=images,
                link_for_download=link_for_download
            )
        )

    return execute(success=True, data=search_result)


@router.get('/news', tags=['News'], status_code=status.HTTP_200_OK)
@router.post('/news', tags=['News'], status_code=status.HTTP_200_OK)
async def news(page: int = 1):
    '''Web service to display news. onnected to the site www.tasnimnews.com'''
    url = 'https://www.tasnimnews.com'
    request = requests.request('GET', f'{url}/fa/top-stories?page={page}')
    if request.status_code != requests.codes.ok:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='A problem has occurred on our end'
        )

    soup = bs4.BeautifulSoup(request.text, 'html.parser')
    articles = soup.find_all('article', class_='list-item')

    search_result = list()
    for article in articles:
        title = article.find('h2', class_='title').text.strip()
        description = article.find('h4').text.strip()
        image = article.find('img', src=True)
        full_url = article.find('a', href=True)
        search_result.append(
            dict(
                title=title,
                description=description,
                url=url + full_url['href'],
                image=image['src']
            )
        )

    return execute(success=True, data=search_result)


@router.get('/rubino', tags=['Social media'], status_code=status.HTTP_200_OK)
@router.post('/rubino', tags=['Social media'], status_code=status.HTTP_200_OK)
async def rubino(auth: str, url: str, timeout: float = 10):
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
async def translate(text: str, to_lang: str = 'auto', from_lang: str = 'auto'):
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
async def github_topic_search(query: str, per_page: int = 30, page: int = 1):
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
        sort: str = 'stars',
        order: str = 'desc',
        per_page: int = 30,
        page: int = 1
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
        sort: str = 'followers',
        order: str = 'desc',
        per_page: int = 30,
        page: int = 1,
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
async def icon(query: str, page: int = 1):
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
async def b64(text : str):
    b_string = codecs.encode(text, 'utf-8')
    output = base64.b64encode(b_string)


@router.get('/bs64decode', tags=['Base64'], status_code=status.HTTP_200_OK)
@router.post('/bs64decode', tags=['Base64'], status_code=status.HTTP_200_OK)
async def b64encode(text : str):
    b_string = codecs.encode(text, 'utf-8')
    try:
        output = base64.b64decode(b_string)
        return execute(success=True, data=output)
    except:
        return execute(success=False, data='This Text Not Base64')
