from fastapi import FastAPI, status

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

class HeroAPI:

    def __init__(
            self,
            url: str = 't.me/Heroapi',
            developer: str = 'amirali irvany',
        github: str = 'https://github.com/metect/Heroapi'
    ) -> dict:
        self.url: str = url
        self.developer: str = developer
        self.github: str = github

    def return_json(
            self,
            data: dict = None,
            status: bool = True,
            developer: str = None,
            err_message: str = None,
    ) -> dict:
        developer = self.developer if developer == None else None
        __dict: dict = {
            'status': status,
            'dev': developer,
            'url': self.url,
            'github': self.github,
            'result': {
                'err_message': err_message,
                'out': data
            },
        }
        return __dict


heroapi = HeroAPI()

@app.get('/', status_code=status.HTTP_200_OK)
async def main() -> dict:
    '''displaying developer information'''
    return heroapi.return_json()


parameters: list = [{'item': 'url', 'item': 'timeout'}]
@app.get('/api/rubino', status_code=status.HTTP_200_OK)
async def rubino_dl(url: str, timeout: float = 10) -> dict:
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
    auth_list: list = []
    payload: dict = {
        'api_version': '0',
        'auth': random.choice(seq=auth_list),
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
    return heroapi.return_json(
        data=session.request('post', url=base_url, timeout=timeout, json=payload).json()
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
        result = converted_text.split('\n')[0:-1]

    return heroapi.return_json(data=result)


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
        return heroapi.return_json(
            data=langdetect.detect(text)
        )
    except langdetect.LangDetectException:
        return heroapi.return_json(
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
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0'
        }
    )

    if r.status_code == 200:
        result = re.findall(r'(?s)class="(?:t0|result-container)">(.*?)<', r.text)
        return heroapi.return_json(
            data=html.unescape(result[0])
        )
    else:
        return heroapi.return_json(
            err_message='A problem has occurred on our end'
        )


# parameters: list = [{'item': 'p'}]
# @app.get('/api/text2image', status_code=status.HTTP_200_OK)
# async def text2image(p: str) -> dict:
#     '''This api is used to convert text to image by artificial intelligence'''
#     url: str = replicate.run(
#         'stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b',
#         input={
#             'prompt': p
#         }
#     )
#     return heroapi.return_json(
#         data={
#             'prompt': p,
#             'url': url[0]
#         }
#     )


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
        return heroapi.return_json(
            err_message='The amount is too big. Send a smaller number `count`'
        )
    else:
        return heroapi.return_json(
            data=faker.Faker([lang]).text()
        )


@app.get('/api/datetime', status_code=status.HTTP_200_OK)
async def datetime() -> dict:
    '''This api is used to display date and time in solar'''
    return heroapi.return_json(
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
    gold = re.findall(r'.*\">(.*)<\/', string=str(html[3]))
    dollar = re.findall(r'.*\">(.*)<\/', string=str(html[5]))
    euro = re.findall(r'.*\">(.*)<\/', string=str(html[6]))
    bitcoin = re.findall(r'.*\">(.*)<\/', string=str(html[8]))
    return heroapi.return_json(
        data={
            'gold18': gold[0],
            'dollar': dollar[0],
            'euro': euro[0],
            'bitcoin': bitcoin[0]
        }
    )
