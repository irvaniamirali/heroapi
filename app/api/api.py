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
import moviepy.editor

class HeroAPI:

    def __init__(
            self,
            url: str = 'https://t.me/HeroAPI',
            developer: str = 'amirali irvany',
            github: str = 'https://github.com/metect/HeroAPI'
    ) -> None:
        self.url: str = url
        self.developer: str = developer
        self.github: str = github

    async def execute(
            self,
            status: bool = True,
            developer: str = None,
            err_message: str = None,
            data: dict = None,
    ) -> dict:
        developer = self.developer if developer == None else self.developer
        return {
            'success': status,
            'dev': developer,
            'url': self.url,
            'github': self.github,
            'result': {
                'out': data,
                'err_message': err_message,
            }
        }


    async def location(self, text: str, latitude: int, longitude: int) -> dict:
        access_key: str = os.getenv(key='NESHAN_KEY')
        base_url_api: str = f'https://api.neshan.org/v1/search?term={text}&lat={latitude}&lng={longitude}'
        r = requests.request(
            method='get', url=base_url_api, headers={
                'Api-Key': access_key
            }
        )
        if r.status_code == 200:
            final_value: dict = r.json()
            return await self.execute(status=True, data=final_value)
        else:
            return await self.execute(status=False, err_message='A problem occurred on the server side')


    async def datetime(self, tr_num: str) -> dict:
        current_date = jalali.Jalalian.jdate('H:i:s ,Y/n/j', tr_num=tr_num)
        return await self.execute(status=True, data=current_date)


    async def ascii_art(self, image: bytes) -> dict:
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
        return await self.execute(data='\n'.join(ascii_image))


    async def translate(self, text: str, to_lang: str, from_lang: str) -> dict:
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
            return await self.execute(status=True, data=html.unescape(result[0]))
        else:
            return await self.execute(status=False, data='A problem has occurred on our end')


    async def rubino(self, auth: str, url: str, timeout: float) -> dict:
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
        return await self.execute(data=responce.json())


    async def language_detect(self, text: str) -> dict:
        try:
            return await self.execute(data=langdetect.detect(text))
        except langdetect.LangDetectException:
            return await self.execute(
                status=False,
                err_message='The value of the `text` parameter is not invalid'
            )


    async def font(self, text: str) -> dict:
        if langdetect.detect(text) in ['fa', 'ar', 'ur']:
            return await self.execute(
                status=False, err_message='Currently, Persian language is not supported'
            )
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
                result = converted_text.split('\n')[0:-1]

            return await self.execute(data=result)


    async def joke(self, mode: str) -> dict:
        with open('app/jsonfiles/joke.json', 'r') as f:
            data = json.load(f)['data']

        if mode == 'random':
            joke = random.choice(seq=data)
            return await self.execute(data=joke.strip())
        elif mode == 'full':
            return await self.execute(data=data)


    async def bard_ai(self, prompt: str) -> dict:
        base_url: str = 'https://api.safone.dev/'
        responce = requests.request(
            method='get', url=f'{base_url}bard?message={prompt}'
        )
        if responce.status_code == 200:
            final_responce = responce.json()
            ai_responce = final_responce['candidates'][0]['content']['parts'][0]['text']
            return await self.execute(status=True, data=ai_responce)
        else:
            return await self.execute(status=False, err_message='A problem has occurred on our end')


    async def fake_text(self, count: str, lang: str) -> dict:
        MAX_VALUE = 999
        if count >= MAX_VALUE:
            return await self.execute(
                status=False, err_message='The amount is too big. Send a smaller number `count`'
            )
        else:
            return await self.execute(data=faker.Faker([lang]).text(count))


    async def news(self) -> dict:
        request = requests.request(
            'get', f'https://www.tasnimnews.com/fa/top-stories'
        )
        rand_num = random.randint(0, 9)
        build_data = lambda value : value[rand_num].strip()
        # parser data from website https://www.tasnimnews.com/fa/top-stories
        title = re.findall(r'<h2 class=\"title \">(.*?)</h2>', request.text)
        description = re.findall(r'<h4 class=\"lead\">(.*?)</h4>', request.text)
        time = re.findall(r'<time><i class=\"fa fa-clock-o\"></i>(.*?)</time>', request.text)
        full_url = re.findall('<article class=\"list-item \"><a href=\"(.*?)\">', request.text)
        return await self.execute(
            data={
                'title': re.sub('&quot', '', build_data(title)),
                'description': build_data(description),
                'time': build_data(time),
                'full_url': f'https://www.tasnimnews.com{build_data(full_url)}',
            }
        )


    async def video_to_mp3(self, video) -> dict:
        FILE_PATH = 'app/tmpfiles/video.mp4'
        with open(FILE_PATH, 'wb') as file:
            file.write(video)

        video = moviepy.editor.VideoFileClip(FILE_PATH)
        video.audio.write_audiofile('app/tmpfiles/sound.mp3')
