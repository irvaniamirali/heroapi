from fastapi import FastAPI, status
from fastapi.templating import Jinja2Templates

import urllib.parse
import replicate
import html
import re
import requests
import langdetect
import faker
import os
import random
import json
from jalali.Jalalian import jdate
import bs4

app = FastAPI()
templates = Jinja2Templates(directory='templates')


class HeroAPI:

    def __init__(
            self,
            url: str = 't.me/Heroapi',
            developer: str = 'amirali irvany',
            github: str = 'https://github.com/metect/Heroapi'
    ) -> dict:
        self.url: str = url
        self.github: str = github
        self.developer: str = developer

    def execute(
            self,
            status: bool = True,
            developer: str = None,
            err_message: str = None,
            note: str = None,
            data: dict = None,
    ) -> dict:
        developer = self.developer if developer == None else None
        __dict: dict = {
            'status': status,
            'dev': developer,
            'url': self.url,
            'github': self.github,
            'result': {
                'out': data,
                'note': note,
                'err_message': err_message,
            },
        }
        return __dict


heroapi = HeroAPI()

@app.exception_handler(404)
async def custom_404_handler(request, __) -> 'template page':
    return templates.TemplateResponse(
        '404.html', {
            'request': request
        }
    )


@app.get('/', status_code=status.HTTP_200_OK)
async def main() -> dict:
    '''displaying developer information'''
    return heroapi.execute(
        status=True,
        developer='amirali irvany',
        note='This api is available for free and open source. For more information, check the LICENSE file in the repository of this project'
    )


parameters: list = [{'item': 'auth', 'item': 'url', 'item': 'timeout'}]
@app.get('/api/rubino', status_code=status.HTTP_200_OK)
async def rubino_dl(auth: str, url: str, timeout: float = 10) -> dict:
    '''This method is used to get the download link
    and other information of the post(s) in Rubino Messenger
    :param url:
        The link of the desired post
    :param timeout:
        Optional To manage slow timeout when the server is slow
    :return:
        Full post information

    If you want more details, go to this address: https://github.com/metect/myrino
    '''
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
    session = requests.session()
    base_url: str = f'https://rubino{random.randint(1, 20)}.iranlms.ir/'
    return heroapi.execute(
        note='Currently this api is not available'
    )


parameters: list = [{'item': 'text'}]
@app.get('/api/font', status_code=status.HTTP_200_OK)
async def font_generate(text: str) -> dict:
    '''This function is for generating fonts. Currently only English language is supported
    :param text:
        The text you want the font to be applied to
    '''
    prefix = re.sub(pattern='main.py', repl='.f.json', string=os.path.abspath(__file__))
    with open(prefix, 'r') as f:
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
        __global = converted_text.split('\n')[0:-1]

    return heroapi.execute(
        data=__global,
        note='Currently, Persian language is not supported'
    )


parameters: list = [{'item': 'text'}]
@app.get('/api/lang', status_code=status.HTTP_200_OK)
async def lang_detect(text: str) -> dict:
    '''This function is to identify the language of a text
    :param text:
        Your desired text
    :return:
        example: `en` or `fa`

    Powered by the `langdetetc` library
    '''
    try:
        return heroapi.execute(
            data=langdetect.detect(text)
        )
    except langdetect.LangDetectException:
        return heroapi.execute(
            err_message='The value of the `text` parameter is not invalid'
        )


parameters: list = [{'item': 'text', 'item': 'to_lang', 'item': 'from_lang'}]
@app.get('/api/translate', status_code=status.HTTP_200_OK)
async def translate(text: str, to_lang: str = 'auto', from_lang: str = 'auto') -> dict:
    '''This API, which is based on the Google Translate API, is used to translate texts'''
    session = requests.session()
    base_url: str = 'https://translate.google.com'
    url: str = f'{base_url}/m?tl={to_lang}&sl={from_lang}&q={urllib.parse.quote(text)}'
    r = session.request(
        method='get', url=url, headers={
            'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0'
        }
    )

    if r.status_code == 200:
        result = re.findall(r'(?s)class="(?:t0|result-container)">(.*?)<', r.text)
        return heroapi.execute(
            data=html.unescape(result[0])
        )
    else:
        return heroapi.execute(
            err_message='A problem has occurred on our end'
        )


parameters: list = [{'item': 'count', 'item': 'lang'}]
@app.get('/api/faketext', status_code=status.HTTP_200_OK)
async def fake_text(count: int = 100, lang: str = 'en_US') -> dict:
    '''This api is used to generate fake text
    :param count
        Number of words, example >>> `10`
    :param lang
        desired language, example >>> `en_US` or `fa_IR`

    Power taken from the library `Faker`
    '''
    if count > 999:
        return heroapi.execute(
            err_message='The amount is too big. Send a smaller number `count`'
        )
    else:
        return heroapi.execute(
            data=faker.Faker([lang]).text()
        )


@app.get('/api/datetime', status_code=status.HTTP_200_OK)
async def datetime() -> dict:
    '''This api is used to display date and time in solar'''
    return heroapi.execute(
        data=jdate(result_format='H:i:s ,Y/n/j')
    )


@app.get('/api/usd', status_code=status.HTTP_200_OK)
async def usd() -> dict:
    '''api to get live currency prices from the `https://irarz.com`
    > More details will be added soon
    '''
    r = requests.get(
        'https://www.tgju.org/currency'
    )
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    html = soup.find_all(
        'span', {
            'class': 'info-price'
        }
    )
    __make = lambda tag_number : re.findall(r'.*\">(.*)<\/', string=str(html[tag_number]))[0]

    return heroapi.execute(
        data={
            'exchange': __make(0),
            'shekel_gold': __make(2),
            'gold18': __make(3),
            'dollar': __make(5),
            'euro': __make(6),
            'Brent_oil': __make(7),
            'bitcoin': __make(8)
        }
    )
