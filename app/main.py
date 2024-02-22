from fastapi import FastAPI, status
from .api.api import *


app = FastAPI()

@app.get('/', status_code=status.HTTP_200_OK)
async def main() -> dict:
    '''displaying developer information'''
    return {
        'status': True,
        'dev': 'amirali irvany',
        'url': 't.me/Heroapi'
    }


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
    # result: dict = rubino(url=url, timeout=timeout)
    return {
        'status': True,
        'dev': 'amirali irvany',
        'url': 't.me/Heroapi',
        'result': 'Currently, it is not possible to use this web service'
    }


parameters: list = [{'item': 'text'}]
@app.get('/api/font', status_code=status.HTTP_200_OK)
async def font_generate(text: str) -> dict:
    '''This function is for generating fonts. Currently only English language is supported
    :param text:
        The text you want the font to be applied to
    '''
    if lang(text) in ['fa', 'ar']:
        return 'Currently, Persian language is not supported'

    result: list = font(text=text)
    return {
        'status': True,
        'dev': 'amirali irvany',
        'url': 't.me/Heroapi',
        'result': result
    }


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
    result: str = lang(text=text)
    return {
        'status': True,
        'dev': 'amirali irvany',
        'url': 't.me/Heroapi',
        'result': result
    }


parameters: list = [{'item': 'text', 'item': 'to_lang', 'item': 'from_lang'}]
@app.get('/api/translate', status_code=status.HTTP_200_OK)
async def translate(text: str, to_lang: str = 'auto', from_lang: str = 'auto') -> dict:
    '''This API, which is based on the Google Translate API, is used to translate texts'''
    result: str = translator(text=text, to_lang=to_lang, from_lang=from_lang)
    return {
        'status': True,
        'dev': 'amirali irvany',
        'url': 't.me/Heroapi',
        'result': result
    }


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
    return {
        'status': True,
        'dev': 'amirali irvany',
        'url': 't.me/Heroapi',
        'result': {
            'prompt': p,
            'url': url[0]
        }
    }


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
    if count > 999:
        return {
            'err-message': 'The amount is too big. Send a smaller number'
        }

    result: str = fake(count=count, lang=lang)
    return {
        'status': True,
        'dev': 'amirali irvany',
        'url': 't.me/Heroapi',
        'result': result
    }
