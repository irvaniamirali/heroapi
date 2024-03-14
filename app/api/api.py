from ast import literal_eval
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
import jdatetime

class HeroAPI:
    def __init__(self):
        pass


    async def execute(
            self,
            success: bool = True,
            dev: str = 'Hero Team',
            url: str = 'https://t.me/HeroAPI',
            github: str = 'https://github.com/metect/HeroAPI',
            data: dict = None,
            err_message: str = None
    ) -> dict:
        return dict(
            success=success,
            dev=dev,
            url=url,
            github=github,
            data=data,
            err_message=err_message
        )


    async def bard_ai(self, prompt: str):
        url: str = 'https://api.safone.dev/'
        request = requests.request(method='GET', url=f'{url}bard?message={prompt}')
        if request.status_code != requests.codes.ok:
            return await self.execute(success=False, err_message='A problem has occurred on our end')

        final_responce = request.json()
        responce = final_responce['candidates'][0]['content']['parts'][0]['text']
        return await self.execute(success=True, data=responce)


    async def asci_art(self, image: bytes):
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
        return await self.execute(success=True, data='\n'.join(ascii_image))


    async def font(self, text: str):
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


    async def datetime(self):
        current_date = jalali.Jalalian.jdate('H:i:s ,Y/n/j', tr_num=tr_num)
        return await self.execute(success=True, data=current_date)

    async def faker(self, item: str, count: int, lang: str):
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
