from fastapi import FastAPI, Request, File, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.api.api import ohmyapi

# Instances
api = ohmyapi()
app = FastAPI(
    title='ohmyapi',
    description='Free and open source api',
    contact={
        'name': 'amirali irvany',
        'url': 'https://metect.github.io',
        'email': 'dev.amirali.irvany@gmail.com',
    },
    terms_of_service='https://t.me/ohmyapi',
    license_info={
        'name': 'Released under MIT LICENSE',
        'url': 'https://spdx.org/licenses/MIT.html'
    },
    docs_url=None,
    redoc_url=None
)

templates = Jinja2Templates(directory='app/templates')
app.mount('/app/static', StaticFiles(directory='app/static'), name='static')

limiter = Limiter(key_func=get_remote_address)
app.state.limiter, LIMITER_TIME = limiter, '1000/minute'
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


async def execute(success: bool = True, data: dict = None, err_message: str = None) -> dict:
    '''Making outter json for responce web services'''
    return dict(
        success=success,
        dev='amirali irvany',
        url='https://t.me/ohmyapi',
        github='https://github.com/metect/ohmyapi',
        data=data,
        err_message=err_message
    )


@app.get('/docs', include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url='/openapi.json',
        title='ohmyapi',
        swagger_favicon_url='app/static/favicon.png',
    )


@app.exception_handler(status.HTTP_404_NOT_FOUND)
async def custom_404_handler(request: Request, __):
    return templates.TemplateResponse(
        '404.html', {
            'request': request
        }
    )


@app.get('/api/bard', tags=['AI'], status_code=status.HTTP_200_OK)
@app.post('/api/bard', tags=['AI'], status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def bard_ai(request: Request, prompt: str) -> dict:
    '''Bard artificial intelligence web service'''
    return await api.bard(prompt=prompt)


@app.get('/api/font', tags=['Art'], status_code=status.HTTP_200_OK)
@app.post('/api/font', tags=['Art'], status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def font(request: Request, text: str) -> dict:
    '''Generate ascii fonts. Currently only English language is supported'''
    return await api.font(text=text)


@app.get('/api/datetime', tags=['Data & time'], status_code=status.HTTP_200_OK)
@app.post('/api/datetime', tags=['Data & time'], status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def datetime(request: Request, tr_num: str = 'en') -> dict:
    '''Display detailed information about the date of the solar calendar'''
    return await api.datetime(tr_num=tr_num)


@app.get('/api/convert-date', tags=['Date & time'], status_code=status.HTTP_200_OK)
@app.post('/api/convert-date', tags=['Date & time'], status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def convert_date(request: Request, day: int, month: int, year: int) -> dict:
    return await api.convert_date(day=day, month=month, year=year)


@app.get('/api/faker', tags=['Fake data'], status_code=status.HTTP_200_OK)
@app.post('/api/faker', tags=['Fake data'], status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def fake_text(request: Request, item: str, count: int = 100, lang: str = 'en') -> dict:
    '''Production fake data. items: (`text`, `text`, `email`)'''
    MAXIMUM_REQUEST: int = 100
    if count > MAXIMUM_REQUEST:
        return await execute(
            success=False, err_message='The amount is too big. Send a smaller number `count`'
        )
    else:
        final_values = list()
        if item == 'text':
            return await execute(success=True, data=faker.Faker([lang]).text(count))
        elif item == 'name':
            for i in range(count):
                final_values.append(faker.Faker([lang]).name())

        elif item == 'email':
            for i in range(count):
                final_values.append(faker.Faker([lang]).email())

    return await execute(success=True, data=final_values)


@app.get('/api/lang', tags=['Identify language'], status_code=status.HTTP_200_OK)
@app.post('/api/lang', tags=['Identify language'], status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def language_detect(request: Request, text: str) -> dict:
    '''Identifying the language of texts'''
    try:
        result_detected = langdetect.detect(text)
        return await execute(success=True, data=result_detected)
    except langdetect.LangDetectException:
        return await execute(
            success=False,
            err_message='The value of the `text` parameter is not invalid'
        )


@app.get('/api/location', tags=['Location'], status_code=status.HTTP_200_OK)
@app.post('/api/location', tags=['Location'], status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def location(request: Request, text: str, latitude: float, longitude: float) -> dict:
    '''Web service to get location and map'''
    access_key = os.getenv(key='NESHAN_KEY')
    url = f'https://api.neshan.org/v1/search?term={text}&lat={latitude}&lng={longitude}'
    request = requests.request(
        method='GET', url=url, headers={
            'Api-Key': access_key
        }
    )
    if request.status_code != requests.codes.ok:
        return await execute(
            success=False, err_message='A problem occurred on the server side'
        )

    return await execute(success=True, data=request.json())


@app.get('/api/music-fa', tags=['Music search'], status_code=status.HTTP_200_OK)
@app.post('/api/music-fa', tags=['Music search'], status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def music_fa(request: Request, query: str, page: int = 1) -> dict:
    '''Search and search web service on the [music-fa](https://music-fa.com) site'''
    request = requests.request('GET', f'https://music-fa.com/search/{query}/page/{page}')
    if request.status_code != requests.codes.ok:
        return await execute(success=False, data='A problem has occurred on our end')

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

    return await execute(success=True, data=search_result)


@app.get('/api/news', tags=['News'], status_code=status.HTTP_200_OK)
@app.post('/api/news', tags=['News'], status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def news(request: Request, page: int = 1) -> dict:
    '''Web service to display news. onnected to the site www.tasnimnews.com'''
    url = 'https://www.tasnimnews.com'
    request = requests.request('GET', f'{url}/fa/top-stories?page={page}')
    if request.status_code != requests.codes.ok:
        return await execute(success=False, data='A problem has occurred on our end')

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

    return await execute(success=True, data=search_result)


@app.get('/api/rubino', tags=['Social media'], status_code=status.HTTP_200_OK)
@app.post('/api/rubino', tags=['Social media'], status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def rubino(request: Request, auth: str, url: str, timeout: float = 10) -> dict:
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
        return await execute(success=False, data='A problem has occurred on our end')

    return await execute(success=True, data=request.json())


@app.get('/api/translate', tags=['Translate'], status_code=status.HTTP_200_OK)
@app.post('/api/translate', tags=['Translate'], status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def translate(request: Request, text: str, to_lang: str = 'auto', from_lang: str = 'auto') -> dict:
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
        return await execute(success=False, data='A problem has occurred on our end')

    result = re.findall(r'(?s)class="(?:t0|result-container)">(.*?)<', request.text)
    return await execute(success=True, data=html.unescape(result[0]))


@app.get('/api/github-topic-search', tags=['Github'], status_code=status.HTTP_200_OK)
@app.post('/api/github-topic-search', tags=['Github'], status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def github_topic_search(request: Request, query: str, per_page: int = 30, page: int = 1) -> dict:
    '''Github topic search web service'''
    headers = {
        'Accept': 'application/vnd.github+json'
    }
    url = 'https://api.github.com/search/topics?q=%s&per_page=%s&page=%s'
    request = requests.request(method='GET', url=url % (query, per_page, page), headers=headers)
    if request.status_code != requests.codes.ok:
        return await execute(success=False, data='A problem has occurred on our end')

    return await execute(success=True, data=request.json())


@app.get('/api/github-repo-search', tags=['Github'], status_code=status.HTTP_200_OK)
@app.post('/api/github-repo-search', tags=['Github'], status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def github_repo_search(
        request: Request,
        name: str,
        sort: str = 'stars',
        order: str = 'desc',
        per_page: int = 30,
        page: int = 1
) -> dict:
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
        return await execute(success=False, data='A problem has occurred on our end')

    return await execute(success=True, data=request.json())


@app.get('/api/github-users-search', tags=['Github'], status_code=status.HTTP_200_OK)
@app.post('/api/github-users-search', tags=['Github'], status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def github_users_search(
        request: Request,
        query: str,
        sort: str = 'followers',
        order: str = 'desc',
        per_page: int = 30,
        page: int = 1,
) -> dict:
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
        return await execute(success=False, data='A problem has occurred on our end')

    return await execute(success=True, data=request.json())


@app.get('/api/pypi', tags=['PyPi'], status_code=status.HTTP_200_OK)
@app.post('/api/pypi', tags=['PyPi'], status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def pypi_search(request: Request, query: str) -> dict:
    '''PyPi package search web service'''
    query = '+'.join(query.split())
    request = requests.request(method='GET', url=f'https://pypi.org/search/?q={query}')
    if request.status_code != requests.codes.ok:
        return await execute(success=False, data='A problem has occurred on our end')

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

    return await execute(success=True, data=search_results)
