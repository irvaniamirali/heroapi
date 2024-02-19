import urllib.parse
import html
import re
import requests
import random
import langdetect
import faker
import json


def rubino(url: str, timeout: float = 10) -> dict:
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
    return session.request('post', url=base_url, timeout=timeout, json=payload).json()


def font(text: str = 'ohmyapi') -> dict:
    '''This function is for generating fonts. Currently only English language is supported
    :param text:
        The text you want the font to be applied to
    '''

    # opening `f.json` to read the source fonts from it
    with open('.f.json', 'r') as f:
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


def lang(text: str) -> str:
    '''This function is to identify the language of a text
    :param text:
        Your desired text
    :return:
        example: `en` or `fa`
    '''
    return langdetect.detect(text)


def faker_data(content: str = 'text', count: int = 10, lang: str = 'en_US') -> list:
    '''This api is used to generate fake content.
    :param content:
        Type of content. example > `text` or `name`
    :param count:
        Number of contents. example > 10 or 50
    :param lang:
        desired language. example > `en_US` or `fa_IR`
        !NOTE: Uppercase and lowercase letters are sensitive
    :return:
        Fake data as a list
    '''
    data: list = []
    fake: classmethod = faker.Faker(lang.split())
    if content == 'text': return fake.text()
    elif content == 'name':
        for _ in range(0, len(count)):
            data.append(fake.name())

        return data


    elif content == 'data':
        for _ in range(0, len(count)):
            data.append(fake.data())

        return data


    elif content == 'emoji':
        for _ in range(0, len(count)):
            data.append(fake.emoji())

        return data


    elif content == 'ip':
        for _ in range(0, len(count)):
            data.append(fake.ipv4())

        return data


def translate(text: str, to_lang: str = 'auto', from_lang: str = 'auto') -> dict:
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
        return html.unescape(result[0])
    else:
        return 'A problem has occurred'
