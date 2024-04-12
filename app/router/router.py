from fastapi import APIRouter, Response, File, status
from fastapi.responses import FileResponse

from typing import Annotated, Optional
import requests
import bs4
import re
import base64
import codecs
from PIL import Image


router = APIRouter(prefix='/api')

@router.get('/bard', tags=['AI'], status_code=status.HTTP_200_OK)
@router.post('/bard', tags=['AI'], status_code=status.HTTP_200_OK)
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


@router.get('/datetime', tags=['Date & time'], status_code=status.HTTP_200_OK)
@router.post('/datetime', tags=['Date & time'], status_code=status.HTTP_200_OK)
async def datetime(tr_num: Optional[str] = 'en') -> dict:
    '''Display detailed information about the date of the solar calendar'''
    current_date = jdate('H:i:s ,Y/n/j', tr_num=tr_num)
    return {
        'success': True,
        'data': current_date
    }


@router.get('/convert-date', tags=['Date & time'], status_code=status.HTTP_200_OK)
@router.post('/convert-date', tags=['Date & time'], status_code=status.HTTP_200_OK)
async def convert_date(day: int, month: int, year: int) -> dict:
    '''Convert Shamsi date to Gregorian'''
    result_date = date(day=day, month=month, year=year).togregorian()
    return {
        'success': True,
        'data': current_date
    }


@router.get('/font', tags=['Art'], status_code=status.HTTP_200_OK)
@router.post('/font', tags=['Art'], status_code=status.HTTP_200_OK)
async def font(responce: Response, text: Optional[str] = 'HeroAPI') -> dict:
    '''Generate ascii fonts. Currently only English language is supported'''
    if langdetect.detect(text) in ['fa', 'ar', 'ur']:
        responce.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'success': False, 'error_message': 'Currently, Persian language is not supported'
        }
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

        return {
            'success': True,
            'data': final_values
        }

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
    url = f'https://api.neshan.org/v1/search?term={text}&lat={latitude}&lng={longitude}'
    request = requests.request(
        method='GET', url=url, headers={
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

@router.get('/lang', tags=['Language Detect'], status_code=status.HTTP_200_OK)
@router.post('/lang', tags=['Language Detect'], status_code=status.HTTP_200_OK)
async def language_detect(responce: Response, text: str) -> dict:
    '''Identifying the language of texts'''
    try:
        result_detected = langdetect.detect(text)
        return {
            'success': True,
            'data': result_detected
        }
    except langdetect.LangDetectException:
        responce.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'success': False,
            'error_message': 'The value of the `text` parameter is not invalid'
        }


@router.get('/location', tags=['Location'], status_code=status.HTTP_200_OK)
@router.post('/location', tags=['Location'], status_code=status.HTTP_200_OK)
async def location(
        responce: Response,
        text: str,
        latitude: Optional[float] = 0,
        longitude: Optional[float] = 0
) -> dict:
    '''Web service to get location and map'''
    access_key = os.getenv(key='NESHAN_KEY')
    url = f'https://api.neshan.org/v1/search?term={text}&lat={latitude}&lng={longitude}'
    request = requests.request(
        method='GET', url=url, headers={
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


@router.get('/news', tags=['News'], status_code=status.HTTP_200_OK)
@router.post('/news', tags=['News'], status_code=status.HTTP_200_OK)
async def news(responce: Response, page: Optional[int] = 1) -> dict:
    '''Web service to display news. onnected to the site www.tasnimnews.com'''
    url = 'https://www.tasnimnews.com'
    request = requests.request('GET', f'{url}/fa/top-stories?page={page}')
    if request.status_code != requests.codes.ok:
        responce.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'success': False, 'error_message': 'A problem has occurred on our end'
        }

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

    return {
        'success': True,
        'data': search_result
    }


@router.get('/github-topic-search', tags=['Github'], status_code=status.HTTP_200_OK)
@router.post('/github-topic-search', tags=['Github'], status_code=status.HTTP_200_OK)
async def github_topic_search(
        responce: Response,
        query: str,
        per_page: Optional[int] = 30,
        page: Optional[int] = 1
) -> dict:
    '''Github topic search web service'''
    headers = {
        'Accept': 'application/vnd.github+json'
    }
    url = 'https://api.github.com/search/topics?q=%s&per_page=%s&page=%s'
    request = requests.request(method='GET', url=url % (query, per_page, page), headers=headers)
    if request.status_code != requests.codes.ok:
        responce.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'success': False, 'error_message': 'A problem has occurred on our end'
        }

    return {
        'success': True,
        'data': request.json()
    }


@router.get('/github-repo-search', tags=['Github'], status_code=status.HTTP_200_OK)
@router.post('/github-repo-search', tags=['Github'], status_code=status.HTTP_200_OK)
async def github_repo_search(
        responce: Response,
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
        responce.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'success': False, 'error_message': 'A problem has occurred on our end'
        }

    return {
        'success': True,
        'data': request.json()
    }


@router.get('/github-users-search', tags=['Github'], status_code=status.HTTP_200_OK)
@router.post('/github-users-search', tags=['Github'], status_code=status.HTTP_200_OK)
async def github_users_search(
        responce: Response,
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
        responce.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'success': False, 'error_message': 'A problem has occurred on our end'
        }

    return {
        'success': True,
        'data': request.json()
    }


@router.get('/pypi', tags=['PyPi'], status_code=status.HTTP_200_OK)
@router.post('/pypi', tags=['PyPi'], status_code=status.HTTP_200_OK)
async def pypi_package_search(responce: Response, query: str) -> dict:
    '''PyPi package search web service'''
    query = '+'.join(query.split())
    request = requests.request(method='GET', url=f'https://pypi.org/search/?q={query}')
    if request.status_code != requests.codes.ok:
        responce.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'success': False, 'error_message': 'A problem has occurred on our end'
        }

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

    return {
        'success': True,
        'data': search_results
    }


@router.get('/icon', tags=['Icon'], status_code=status.HTTP_200_OK)
@router.post('/icon', tags=['Icon'], status_code=status.HTTP_200_OK)
async def icon(responce: Response, query: str, page: Optional[int] = 1) -> dict:
    '''Get the icon from icon-icons.com'''
    request = requests.request(method='GET', url=f'https://icon-icons.com/search/icons/?filtro={query}')
    if request.status_code != requests.codes.ok:
        responce.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'success': False, 'error_message': 'A problem has occurred on our end'
        }

    soup = bs4.BeautifulSoup(request.text, 'html.parser')
    icons = soup.find_all('div', class_='icon-preview')

    search_result = list()
    for icon in icons:
        data_original = icon.find('img', class_='lazy', src=True)
        search_result.append(data_original['data-original'])

    return {
        'success': True,
        'data': search_result
    }


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


@router.get('/bs64encode', tags=['Base64'], status_code=status.HTTP_200_OK)
@router.post('/bs64encode', tags=['Base64'], status_code=status.HTTP_200_OK)
async def base64encode(text : str) -> dict:
    b_string = codecs.encode(text, 'utf-8')
    output = base64.b64encode(b_string)
    return {
        'success': True,
        'data': output
    }


@router.get('/bs64decode', tags=['Base64'], status_code=status.HTTP_200_OK)
@router.post('/bs64decode', tags=['Base64'], status_code=status.HTTP_200_OK)
async def b64encode(responce: Response, text : str) -> dict:
    b_string = codecs.encode(text, 'utf-8')
    try:
        output = base64.b64decode(b_string)
        return {
            'success': True,
            'data': output
        }
    except:
        responce.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'success': False, 'error_message': 'This text not base64'
        }


@router.get('/rubino', tags=['Social media'], status_code=status.HTTP_200_OK)
@router.post('/rubino', tags=['Social media'], status_code=status.HTTP_200_OK)
async def rubino(responce: Response, auth: str, url: str, timeout: Optional[float] = 10) -> dict:
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
        responce.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'success': False, 'error_message': 'A problem has occurred on our end'
        }

    return {
        'success': True,
        'data': request.json()
    }


@router.get('/domain-price', tags=['Domain'], status_code=status.HTTP_200_OK)
@router.post('/domain-price', tags=['Domain'], status_code=status.HTTP_200_OK)
async def domain_price(responce: Response) -> dict:
    '''Get Domain price from [parsvds.com](https://parsvds.com) web site'''
    request = requests.request(method='GET', url=f'https://parsvds.com/domain/')
    if request.status_code != requests.codes.ok:
        responce.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'success': False, 'error_message': 'A problem has occurred on our end'
        }

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

    return {
        'success': True,
        'data': search_result
    }


@router.get('/rand-anime', tags=['Anime'], status_code=status.HTTP_200_OK)
@router.post('/rand-anime', tags=['Anime'], status_code=status.HTTP_200_OK)
async def random_anime_image(responce: Response) -> "FileResponse":
    '''Get the icon from icon-icons.com'''
    request = requests.request(method='GET', url='https://pic.re/image')
    if request.status_code != requests.codes.ok:
        responce.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'success': False, 'error_message': 'A problem has occurred on our end'
        }

    with open('app/tmpfiles/anime.png', 'wb+') as _file:
        _file.write(request.content)

    return FileResponse('app/tmpfiles/anime.png')
