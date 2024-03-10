from fastapi import FastAPI, Request, File, status
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from typing import Annotated

from app.api.api import HeroAPI


api = HeroAPI()
app = FastAPI(
    title='HeroAPI',
    description='Free api and web service',
    contact={
        'email': 'dev.amirali.irvany@gmail.com',
    },
    redoc_url=None,
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter, LIMITER_TIME = limiter, '1000/minute'
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.exception_handler(status.HTTP_404_NOT_FOUND)
async def custom_404_handler(request: Request, __):
    templates = Jinja2Templates(directory='app/templates')
    return templates.TemplateResponse(
        '404.html', {
            'request': request
        }
    )

@app.get('/api/font', status_code=status.HTTP_200_OK)
@app.post('/api/font', status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def font(request: Request, text: str) -> dict:
    '''Generate ascii fonts. Currently only English language is supported'''
    return await api.font(text=text)


@app.get('/api/faketext', status_code=status.HTTP_200_OK)
@app.post('/api/faketext', status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def fake_text(request: Request, count: int = 100, lang: str = 'en_US') -> dict:
    '''Production fake text'''
    return await api.fake_text(count=count, lang=lang)


@app.get('/api/rubino', status_code=status.HTTP_200_OK)
@app.post('/api/rubino', status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def rubino(request: Request, auth: str, url: str, timeout: float = 10) -> dict:
    '''This api is used to get the information of the post(s) in Rubino Messenger'''
    return await api.rubino(auth=auth, url=url, timeout=timeout)


@app.get('/api/lang', status_code=status.HTTP_200_OK)
@app.post('/api/lang', status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def language_detect(request: Request, text: str) -> dict:
    '''Identifying the language of texts'''
    return await api.language_detect(text=text)


@app.get('/api/translate', status_code=status.HTTP_200_OK)
@app.post('/api/translate', status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def translate(request: Request, text: str, to_lang: str = 'auto', from_lang: str = 'auto') -> dict:
    '''Translation of texts based on the Google Translate engine'''
    return await api.translate(text=text, to_lang=to_lang, from_lang=from_lang)


@app.get('/api/datetime', status_code=status.HTTP_200_OK)
@app.post('/api/datetime', status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def datetime(request: Request, tr_num: str = 'en') -> dict:
    '''Display detailed information about the date of the solar calendar'''
    return await api.datetime(tr_num=tr_num)


@app.get('/api/location', status_code=status.HTTP_200_OK)
@app.post('/api/location', status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def location(request: Request, text: str, latitude: int, longitude: int) -> dict:
    '''Web service to get location and map'''
    return await api.location(text=text, latitude=latitude, longitude=longitude)


@app.get('/api/image2ascii', status_code=status.HTTP_200_OK)
@app.post('/api/image2ascii', status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def ascii_art(request: Request, image: Annotated[bytes, File()]) -> dict:
    '''Convert image to ascii art'''
    return await api.ascii_art(image=image)


@app.get('/api/bard', status_code=status.HTTP_200_OK)
@app.post('/api/bard', status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def bard_ai(request: Request, prompt: str) -> dict:
    '''Bard artificial intelligence web service'''
    return await api.bard_ai(prompt=prompt)


@app.get('/api/news', status_code=status.HTTP_200_OK)
@app.post('/api/news', status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def news(request: Request) -> dict:
    '''Show random news. Connected to the site www.tasnimnews.com'''
    return await ap@app.get('/api/news', status_code=status.HTTP_200_OK)


@app.get('/api/video2mp3', status_code=status.HTTP_200_OK)
@app.post('/api/video2mp3', status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def video_to_mp3(request: Request, video: Annotated[bytes, File()]):
    '''Remove audio from video web service'''
    FILE_PATH = 'app/tmpfiles/sound.mp3'
    sound_byte =  await api.video_to_mp3(video=video)
    return FileResponse(path=FILE_PATH, filename=FILE_PATH)
