from fastapi import FastAPI, status
from .api.api import *


class HeroAPI:

    def __init__(
            self,
            url: str = 't.me/Heroapi',
            github: str = 'https://github.com/metect/Heroapi',
            developer: str = 'amirali irvany'
    ) -> dict:
        self.url: str = url
        self.github: str = github
        self.developer: str = developer

    def return_data(
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
                'err_mesage': err_message,
                'out': data
            },
        }
        return __dict


app = FastAPI()
heroapi = HeroAPI()

@app.get('/', status_code=status.HTTP_200_OK)
async def main() -> dict:
    '''displaying developer information'''
    return heroapi.return_data()


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
    return heroapi.return_data(
        err_message='Currently, it is not possible to use this web service'
    )


parameters: list = [{'item': 'text'}]
@app.get('/api/font', status_code=status.HTTP_200_OK)
async def font_generate(text: str) -> dict:
    '''This function is for generating fonts. Currently only English language is supported
    :param text:
        The text you want the font to be applied to
    '''
    return heroapi.return_data(
        status=True,
        developer='amirali irvany',
        data=font(text=text)
    )


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
    return heroapi.return_data(data=lang(text=text))


parameters: list = [{'item': 'text', 'item': 'to_lang', 'item': 'from_lang'}]
@app.get('/api/translate', status_code=status.HTTP_200_OK)
async def translate(text: str, to_lang: str = 'auto', from_lang: str = 'auto') -> dict:
    '''This API, which is based on the Google Translate API, is used to translate texts'''
    return heroapi.return_data(
        data=translator(text=text, to_lang=to_lang, from_lang=from_lang)
    )


parameters: list = [{'item': 'p'}]
@app.get('/api/text2image', status_code=status.HTTP_200_OK)
async def text2image(p: str) -> dict:
    '''This api is used to convert text to image by artificial intelligence'''
    url: str = replicate.run(
        'stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b',
        input={
            'prompt': p
        }
    )
    return heroapi.return_data(
        data={
            'prompt': p,
            'url': url[0]
        }
    )


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
    return heroapi.return_data(
        data=fake(count=count, lang=lang)
    )
