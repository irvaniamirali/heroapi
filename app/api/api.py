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



