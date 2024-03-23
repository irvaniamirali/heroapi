import os
import requests
import jalali.Jalalian
import urllib.parse
import re
import html
import langdetect
import json
import random
import faker
import bs4
import jdatetime

class ohmyapi:

    def __init__(
            self,
            dev: str = 'amirali irvany',
            url: str = 'https://t.me/ohmyapi',
            github: str = 'https://github.com/metect/ohmyapi'
    ):
        self.dev = dev
        self.url = url
        self.github = github


    async def execute(self, success: bool = True, data: dict = None, err_message: dict = None) -> dict:
        return dict(
            success=success,
            dev='amirali irvany',
            url='https://t.me/ohmyapi',
            github='https://github.com/metect/ohmyapi',
            data=data,
            err_message=err_message
        )


    async def bard(self, prompt: str) -> dict:
        url = 'https://api.safone.dev/'
        request = requests.request(method='GET', url=f'{url}bard?message={prompt}')
        if request.status_code != requests.codes.ok:
            return await self.execute(success=False, err_message='A problem has occurred on our end')

        responce = request.json()
        final_responce = responce['candidates'][0]['content']['parts'][0]['text']
        return await self.execute(success=True, data=final_responce)


    async def font(self, text: str) -> dict:
        if langdetect.detect(text) in ['fa', 'ar', 'ur']:
            return await self.execute(
                success=False, err_message='Currently, Persian language is not supported'
            )
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

            return await self.execute(success=True, data=final_values)


    async def datetime(self, tr_num: str) -> dict:
        current_date = jalali.Jalalian.jdate('H:i:s ,Y/n/j', tr_num=tr_num)
        return await self.execute(success=True, data=current_date)


    async def convert_date(self, day: int, month: int, year: int) -> dict:
        result_date = jdatetime.date(day=day, month=month, year=year).togregorian()
        return await self.execute(success=True, data=result_date)


    async def fake_data(self, item: str, count: int, lang: str) -> dict:
        MAXIMUM_REQUEST: int = 100
        if count > MAXIMUM_REQUEST:
            return await self.execute(
                success=False, err_message='The amount is too big. Send a smaller number `count`'
            )
        else:
            final_values = list()
            if item == 'text':
                return await self.execute(success=True, data=faker.Faker([lang]).text(count))
            elif item == 'name':
                for i in range(count):
                    final_values.append(faker.Faker([lang]).name())

            elif item == 'email':
                for i in range(count):
                    final_values.append(faker.Faker([lang]).email())

        return await self.execute(success=True, data=final_values)


    async def language_detect(self, text: str) -> dict:
        try:
            result_detected = langdetect.detect(text)
            return await self.execute(success=True, data=result_detected)
        except langdetect.LangDetectException:
            return await self.execute(
                success=False,
                err_message='The value of the `text` parameter is not invalid'
            )


    async def location(self, text: str, latitude: float, longitude: float) -> dict:
        access_key = os.getenv(key='NESHAN_KEY')
        url = f'https://api.neshan.org/v1/search?term={text}&lat={latitude}&lng={longitude}'
        request = requests.request(
            method='GET', url=url, headers={
                'Api-Key': access_key
            }
        )
        if request.status_code != requests.codes.ok:
            return await self.execute(success=False, err_message='A problem has occurred on our end')

        return await self.execute(success=True, data=request.json())


    async def music_fa(self, query: str, page: int) -> dict:
        request = requests.request('GET', f'https://music-fa.com/search/{query}/page/{page}')
        if request.status_code != requests.codes.ok:
            return await self.execute(success=False, data='A problem has occurred on our end')

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

        return await self.execute(success=True, data=search_result)


    async def news(self, page: int) -> dict:
        url = 'https://www.tasnimnews.com'
        request = requests.request('GET', f'{url}/fa/top-stories?page={page}')
        if request.status_code != requests.codes.ok:
            return await self.execute(success=False, data='A problem has occurred on our end')

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

        return await self.execute(success=True, data=search_result)


    async def rubino(self, auth: str, url: str, timeout: str) -> dict:
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
            return await self.execute(success=False, data='A problem has occurred on our end')

        return await self.execute(success=True, data=request.json())


    async def translate(self, text: str, to_lang: str, from_lang: str) -> dict:
        url = 'https://translate.google.com'
        final_url = f'{url}/m?tl={to_lang}&sl={from_lang}&q={urllib.parse.quote(text)}'
        request = requests.request(
            method='GET', url=final_url, headers={
                'User-Agent':
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0'
            }
        )
        if request.status_code != requests.codes.ok:
            return await self.execute(success=False, data='A problem has occurred on our end')

        result = re.findall(r'(?s)class="(?:t0|result-container)">(.*?)<', request.text)
        return await self.execute(success=True, data=html.unescape(result[0]))


    async def github_topic_search(self, query: str, per_page: int = 30, page: int = 1) -> dict:
        headers = {
            'Accept': 'application/vnd.github+json'
        }
        url = 'https://api.github.com/search/topics?q=%s&per_page=%s&page=%s'
        request = requests.request(method='GET', url=url % (query, per_page, page), headers=headers)
        if request.status_code != requests.codes.ok:
            return await self.execute(success=False, data='A problem has occurred on our end')

        return await self.execute(success=True, data=request.json())


    async def github_repo_search(self, name: str, sort: str, order: str, per_page: int, page: int) -> dict:
        headers = {
            'Accept': 'application/vnd.github+json'
        }
        url = 'https://api.github.com/search/repositories?q=%s&s=%s&order=%s&per_page=%s&page=%s'
        request = requests.request(
            method='GET', url=url % (name, sort, order, per_page, page), headers=headers
        )
        if request.status_code != requests.codes.ok:
            return await execute(success=False, data='A problem has occurred on our end')

        return await self.execute(success=True, data=request.json())
