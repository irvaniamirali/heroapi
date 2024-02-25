import re
import html
import requests
import json
import faker
import urllib.parse
import langdetect

from os.path import abspath
from random import randint
from jalali.Jalalian import jdate
from bs4 import BeautifulSoup


class HeroAPI():

    def __init__(
            self,
            url: str = 't.me/Heroapi',
            developer: str = 'amirali irvany',
            github: str = 'https://github.com/metect/Heroapi'
    ) -> dict:
        self.url: str = url
        self.github: str = github
        self.developer: str = developer

    async def execute(
            self,
            status: bool = True,
            developer: str = None,
            err_message: str = None,
            note: str = None,
            data: dict = None,
    ) -> dict:
        developer = self.developer if developer == None else self.developer
        __dict: dict = {
            'status': status,
            'dev': developer,
            'url': self.url,
            'github': self.github,
            'result': {
                'out': data,
                'note': note,
                'err_message': err_message,
            }
        }
        return __dict

    async def _main(self):
        return await self.execute(
            status=True,
            developer='amirali irvany',
            note='This api is available for free and open source. For more information, check the LICENSE file in the repository of this project'
        )


    async def _rubino(self, auth: str, url: str, timeout: float) -> dict:
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
        base_url: str = f'https://rubino{randint(1, 20)}.iranlms.ir/'
        responce = requests.request(
            method='get', url=base_url, json=payload
        )
        return await self.execute(data=responce.json())


    async def _font(self, text: str) -> dict:
        prefix = re.sub(pattern='api.py', repl='f.json', string=abspath(__file__))
        with open(prefix, 'r') as f:
            fonts = json.load(f)

        converted_text = ''
        for count in range(0, len(fonts)):
            for char in text:
                if char.isalpha():
                    char_index = ord(char.lower()) - 97
                    try:
                        converted_text += fonts[str(count)][char_index]
                    except IndexError:
                        return await self.execute(
                            status=False,
                            err_message='Currently, Persian language is not supported'
                        )
                else:
                    converted_text += char

            converted_text += '\n'
            result = converted_text.split('\n')[0:-1]

        return await self.execute(
            data=result, note='Currently only English language is supported'
        )


    async def _lang_detect(self, text: str) -> dict:
        try:
            return await self.execute(data=langdetect.detect(text))
        except langdetect.LangDetectException:
            return await self.execute(
                status=False,
                err_message='The value of the `text` parameter is not invalid'
            )


    async def _translate(self, text: str, to_lang: str, from_lang: str) -> dict:
        base_url: str = 'https://translate.google.com'
        url: str = f'{base_url}/m?tl={to_lang}&sl={from_lang}&q={urllib.parse.quote(text)}'
        r = requests.get(
            url=url, headers={
                'User-Agent':
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0'
            }
        )

        if r.status_code == 200:
            result = re.findall(r'(?s)class="(?:t0|result-container)">(.*?)<', r.text)
            return await self.execute(
                data=html.unescape(result[0])
            )
        else:
            return await self.execute(
                status=False,
                data='A problem has occurred on our end'
            )


    async def _faketext(self, count: int, lang: str) -> dict:
        if count >= 999:
            return await self.execute(
                status=False,
                err_message='The amount is too big. Send a smaller number `count`'
            )
        else:
            return await self.execute(
                data=faker.Faker([lang]).text(count)
            )


    async def _datetime(self, tr_num: str) -> dict:
        return await self.execute(
            data=jdate(result_format='H:i:s ,Y/n/j', tr_num=tr_num)
        )


    async def _usd(self):
        r = requests.get(
            'https://www.tgju.org/currency'
        )
        soup = BeautifulSoup(r.text, 'html.parser')
        html = soup.find_all(
            'span', {
                'class': 'info-price'
            }
        )
        __make = lambda index: re.findall(r'.*\">(.*)<\/', string=str(html[index]))[0]
        return await self.execute(
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


    async def _bard(self, text):
        url: str = 'https://api.safone.dev/bard?message=hello'
        responce = requests.request(method='get', url=url)
        if responce.status_code == 200:
            _json = responce.json()
            return await self.execute(data=_json['candidates'][0]['content']['parts'][0]['text'])
        else:
            return await self.execute(
                status=False,
                err_message='A problem has occurred on our end'
            )


    async def _joke(self):
        prefix = re.sub(pattern='api.py', repl='joke.json', string=abspath(__file__))
        with open(prefix, 'r') as f:
            jokes = json.load(f)

        return await self.execute(
            data=jokes
        )
