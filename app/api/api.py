import urllib.parse
import replicate
import html
import re
import requests
import langdetect
import faker
import os
import json
from jalali.Jalalian import jdate
import bs4


def rubino(url: str, timeout: float = 10) -> dict:
    return
    # auth_list: list = []
    # payload: dict = {
    #     'api_version': '0',
    #     'auth': random.choice(seq=auth_list),
    #     'client': {
    #         'app_name': 'Main',
    #         'app_version': '3.0.1',
    #         'package': 'app.rubino.main',
    #         'lang_code': 'en',
    #         'platform': 'PWA'
    # },
    #     'data': {
    #         'share_link': url.split('/')[-1],
    #         'profile_id': None
    #     },
    #     'method': 'getPostByShareLink'
    # }
    # session = requests.session()
    # base_url: str = f'https://rubino{random.randint(1, 20)}.iranlms.ir/'
    # return session.request('post', url=base_url, timeout=timeout, json=payload).json()


def font(text: str = 'Heroapi') -> dict:
    '''generate ascii font, all fonts: 33'''
    prefix = re.sub(pattern='api.py', repl='f.json', string=os.path.abspath(__file__))
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

    return result


def translator(text: str, to_lang: str = 'auto', from_lang: str = 'auto') -> dict:
    '''This api based on google Translate API, is used to translate texts'''
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
        return html.unescape(result[0])
    else:
        return


def fake(count: int = 100, lang: str = 'en_US') -> str:
    '''This function is used to generate fake text. Power taken from the library `Faker`'''
    return faker.Faker([lang]).text()


def live_usd() -> dict:
    r = requests.get(
        'https://markets.businessinsider.com/currencies/usd-irr'
    )
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    html_string = soup.find(
        'div', {
            'class': 'price-section__values'
        }
    )
    n = re.findall(r'(.*)\..*', re.findall(r'".*\">(.*)</>*', str(html_string))[0])
    return n[0]
