from fastapi import FastAPI, Request, File, status
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from typing import Annotated

from app.api.api import HeroAPI

# Instances
api = HeroAPI()
app = FastAPI(
    title='HeroAPI',
    description='Free and open source api',
    contact={
        'name': 'amirali irvany',
        'url': 'https://metect.github.io',
        'email': 'dev.amirali.irvany@gmail.com',
    },
    terms_of_service='https://t.me/HeroAPI',
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

@app.get('/docs', include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url='/openapi.json',
        title='HeroAPI',
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
    return await api.bard_ai(prompt=prompt)


@app.get('/api/image2ascii', tags=['Art'], status_code=status.HTTP_200_OK)
@app.post('/api/image2ascii', tags=['Art'], status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def ascii_art(request: Request, image: Annotated[bytes, File()]) -> dict:
    '''Convert image to ascii art'''
    return await api.asci_art(image=image)


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


@app.get('/api/faker', tags=['Fake data'], status_code=status.HTTP_200_OK)
@app.post('/api/faker', tags=['Fake data'], status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def fake_text(request: Request, item: str, count: int = 100, lang: str = 'en') -> dict:
    '''Production fake data'''
    return await api.faker(item=item, count=count, lang=lang)


@app.get('/api/lang', tags=['Identify language'], status_code=status.HTTP_200_OK)
@app.post('/api/lang', tags=['Identify language'], status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def language_detect(request: Request, text: str) -> dict:
    '''Identifying the language of texts'''
    return await api.language_detect(text=text)


@app.get('/api/location', tags=['Location'], status_code=status.HTTP_200_OK)
@app.post('/api/location', tags=['Location'], status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def location(request: Request, text: str, latitude: float, longitude: float) -> dict:
    '''Web service to get location and map'''
    return await api.location(text=text, latitude=latitude, longitude=longitude)


@app.get('/api/music-fa', tags=['Music search'], status_code=status.HTTP_200_OK)
@app.post('/api/music-fa', tags=['Music search'], status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def music_fa(request: Request, query: str, page: int = 1) -> dict:
    '''Search and search web service on the [music-fa](https://music-fa.com) site'''
    return await api.music_fa(query=query, page=page)


@app.get('/api/news', tags=['News'], status_code=status.HTTP_200_OK)
@app.post('/api/news', tags=['News'], status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def news(request: Request, page: int = 1) -> dict:
    '''Web service to display news. onnected to the site www.tasnimnews.com'''
    return await api.news(page=page)


@app.get('/api/rubino', tags=['Social media'], status_code=status.HTTP_200_OK)
@app.post('/api/rubino', tags=['Social media'], status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def rubino(request: Request, auth: str, url: str, timeout: float = 10) -> dict:
    '''This api is used to get the information of the post(s) in Rubino Messenger'''
    return await api.rubino(auth=auth, url=url, timeout=timeout)


@app.get('/api/translate', tags=['Translate'], status_code=status.HTTP_200_OK)
@app.post('/api/translate', tags=['Translate'], status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def translate(request: Request, text: str, to_lang: str = 'auto', from_lang: str = 'auto') -> dict:
    '''Translation of texts based on the Google Translate engine'''
    return await api.translator(text=text, from_lang=from_lang, to_lang=to_lang)


@app.get('/api/video2mp3', tags=['Video'], status_code=status.HTTP_200_OK)
@app.post('/api/video2mp3', tags=['Video'], status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def video_to_mp3(request: Request, video: Annotated[bytes, File()]):
    '''Remove audio from video web service'''
    FILE_PATH = await api.video2audio(video=video)
    return FileResponse(path=FILE_PATH, filename=FILE_PATH)


@app.get('/api/github', tags=['Github'], status_code=status.HTTP_200_OK)
@app.post('/api/github', tags=['Github'], status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def github_search(request: Request, query: str, per_page: int = 30, page: int = 1) -> dict:
    '''Github topic search web service'''
    return await api.github_search(query=query, per_page=per_page, page=page)


@app.get('/api/pypi', tags=['PyPi'], status_code=status.HTTP_200_OK)
@app.post('/api/pypi', tags=['PyPi'], status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def pypi_search(request: Request, query: str) -> dict:
    '''PyPi package search web service'''
    return await api.pypi_search(query=query)


@app.get('/api/divar', tags=['Other'], status_code=status.HTTP_200_OK)
@app.post('/api/divar', tags=['Other'], status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def divar(request: Request, query: str, city: str = 'tehran') -> dict:
    '''Web search service in [Divar](https://divar.ir)'''
    return await api.divar_search(query=query, city=city)
