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



