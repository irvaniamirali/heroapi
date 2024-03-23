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
