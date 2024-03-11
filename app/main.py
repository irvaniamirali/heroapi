from fastapi import FastAPI, Request, File, status
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from typing import Annotated
import moviepy.editor
import os
import requests
import jalali.Jalalian
import PIL.Image
import urllib.parse
import re
import html
import langdetect
import json
import random
import faker
import bs4

app = FastAPI(
    title='HeroAPI',
    description='Free and open source api',
    contact={
        'email': 'dev.amirali.irvany@gmail.com',
    },
)

templates = Jinja2Templates(directory='app/templates')
app.mount('/app/static', StaticFiles(directory='app/static'), name='static')

limiter = Limiter(key_func=get_remote_address)
app.state.limiter, LIMITER_TIME = limiter, '1000/minute'
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

async def outter(success: bool, data: dict = None, err_message: str = None) -> dict:
    '''Create json for output'''
    return {
        'success': success,
        'dev': 'amirali irvany',
        'url': 'https://t.me/HeroAPI',
        'github': 'https://github.com/metect/HeroAPI',
        'result': {
            'out': data,
            'err_message': err_message
        },
    }


@app.exception_handler(status.HTTP_404_NOT_FOUND)
async def custom_404_handler(request: Request, __):
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
    if langdetect.detect(text) in ['fa', 'ar', 'ur']:
        return await outter(success=False, err_message='Currently, Persian language is not supported')
    else:
        with open('app/jsonfiles/f.json', 'r') as f:
            fonts = json.load(f)

        converted_text = ''
        for count in range(0, len(fonts)):
            for char in text:
                if char.isalpha():
                    char_index = ord(char.lower()) - 97
                    converted_text += fonts[str(count)][char_index]
                else:
                    converted_text += char

            converted_text += '\n'
            final_values = converted_text.split('\n')[0:-1]

    return await outter(success=True, data=final_values)


@app.get('/api/faketext', status_code=status.HTTP_200_OK)
@app.post('/api/faketext', status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def fake_text(request: Request, count: int = 100, lang: str = 'en_US') -> dict:
    '''Production fake text'''
    MAXIMUM_REQUEST = 999
    if count >= MAXIMUM_REQUEST:
        return await outter(
            success=False, err_message='The amount is too big. Send a smaller number `count`'
        )
    else:
        return await outter(success=True, data=faker.Faker([lang]).text(count))


@app.get('/api/rubino', status_code=status.HTTP_200_OK)
@app.post('/api/rubino', status_code=status.HTTP_200_OK)
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
    base_url: str = f'https://rubino{random.randint(1, 20)}.iranlms.ir/'
    responce = requests.request(
        method='get', url=base_url, json=payload
    )
    return await outter(success=True, data=responce.json())


@app.get('/api/lang', status_code=status.HTTP_200_OK)
@app.post('/api/lang', status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def language_detect(request: Request, text: str) -> dict:
    '''Identifying the language of texts'''
    try:
        return await outter(success=True, data=langdetect.detect(text))
    except langdetect.LangDetectException:
        return await outter(
            success=False,
            err_message='The value of the `text` parameter is not invalid'
        )


@app.get('/api/translate', status_code=status.HTTP_200_OK)
@app.post('/api/translate', status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def translate(request: Request, text: str, to_lang: str = 'auto', from_lang: str = 'auto') -> dict:
    '''Translation of texts based on the Google Translate engine'''
    base_url: str = 'https://translate.google.com'
    final_url: str = f'{base_url}/m?tl={to_lang}&sl={from_lang}&q={urllib.parse.quote(text)}'
    r = requests.request(
        method='get', url=final_url, headers={
            'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0'
        }
    )
    if r.status_code == 200:
        result = re.findall(r'(?s)class="(?:t0|result-container)">(.*?)<', r.text)
        return await outter(success=True, data=html.unescape(result[0]))
    else:
        return await outter(success=False, data='A problem has occurred on our end')


@app.get('/api/datetime', status_code=status.HTTP_200_OK)
@app.post('/api/datetime', status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def datetime(request: Request, tr_num: str = 'en') -> dict:
    '''Display detailed information about the date of the solar calendar'''
    current_date = jalali.Jalalian.jdate('H:i:s ,Y/n/j', tr_num=tr_num)
    return await outter(success=True, data=current_date)


@app.get('/api/location', status_code=status.HTTP_200_OK)
@app.post('/api/location', status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def location(request: Request, text: str, latitude: int, longitude: int) -> dict:
    '''Web service to get location and map'''
    access_key: str = os.getenv(key='NESHAN_KEY')
    base_url: str = f'https://api.neshan.org/v1/search?term={text}&lat={latitude}&lng={longitude}'
    r = requests.request(
        method='get', url=base_url, headers={
            'Api-Key': access_key
        }
    )
    if r.status_code == 200:
        final_value: dict = r.json()
        return await outter(success=True, data=final_value)
    else:
        return await outter(success=False, err_message='A problem occurred on the server side')


@app.get('/api/image2ascii', status_code=status.HTTP_200_OK)
@app.post('/api/image2ascii', status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def ascii_art(request: Request, image: Annotated[bytes, File()]) -> dict:
    '''Convert image to ascii art'''
    with open('app/tmpfiles/image.png', 'wb') as file_byte:
        file_byte.write(image)

    image = PIL.Image.open('app/tmpfiles/image.png')
    width, height = image.size
    aspect_ratio = height / width
    new_height = aspect_ratio * 120 * 0.55
    img = image.resize((120, int(new_height)))

    img = img.convert('L')
    pixels = img.getdata()

    CHARACTERS = ['B', 'S', '#', '&', '@', '$', '%', '*', '!', ':', '.']
    new_pixels = [CHARACTERS[pixel // 25] for pixel in pixels]
    new_pixels, new_pixels_count = ''.join(new_pixels), len(new_pixels)
    ascii_image = [new_pixels[index:index + 120]
    for index in range(0, new_pixels_count, 120)]
    return await outter(success=True, data='\n'.join(ascii_image))


@app.get('/api/bard', status_code=status.HTTP_200_OK)
@app.post('/api/bard', status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def bard_ai(request: Request, prompt: str) -> dict:
    '''Bard artificial intelligence web service'''
    base_url: str = 'https://api.safone.dev/'
    request = requests.request(
        method='get', url=f'{base_url}bard?message={prompt}'
    )
    if request.status_code == 200:
        final_responce = request.json()
        responce = final_responce['candidates'][0]['content']['parts'][0]['text']
        return await outter(success=True, data=responce)
    else:
        return await outter(success=False, err_message='A problem has occurred on our end')


@app.get('/api/news', status_code=status.HTTP_200_OK)
@app.post('/api/news', status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def news(request: Request) -> dict:
    '''Show random news. Connected to the site www.tasnimnews.com'''
    request = requests.request(
        'get', f'https://www.tasnimnews.com/fa/top-stories'
    )
    rand_num = random.randint(0, 9)
    build_data = lambda value: value[rand_num].strip()
    title = re.findall(r'<h2 class=\"title \">(.*?)</h2>', request.text)
    description = re.findall(r'<h4 class=\"lead\">(.*?)</h4>', request.text)
    time = re.findall(r'<time><i class=\"fa fa-clock-o\"></i>(.*?)</time>', request.text)
    full_url = re.findall('<article class=\"list-item \"><a href=\"(.*?)\">', request.text)
    return await outter(
        success=True,
        data={
            'title': re.sub('&quot', '', build_data(title)),
            'description': build_data(description),
            'time': build_data(time),
            'full_url': f'https://www.tasnimnews.com{build_data(full_url)}',
        }
    )


@app.get('/api/video2mp3', status_code=status.HTTP_200_OK)
@app.post('/api/video2mp3', status_code=status.HTTP_200_OK)
@limiter.limit(limit_value=LIMITER_TIME, key_func=get_remote_address)
async def video_to_mp3(request: Request, video: Annotated[bytes, File()]):
    '''Remove audio from video web service'''
    FILE_PATH = 'app/tmpfiles/video.mp4'
    with open(FILE_PATH, 'wb') as file:
        file.write(video)

    video = moviepy.editor.VideoFileClip(FILE_PATH)
    video.audio.write_audiofile('app/tmpfiles/sound.mp3')
    return FileResponse(path=FILE_PATH, filename=FILE_PATH)
