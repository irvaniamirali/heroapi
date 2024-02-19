'''this is `ohmyapi`, free and open-source api'''

from fastapi import FastAPI, status
from api.api import *


app = FastAPI()

@app.get('/', status_code=status.HTTP_200_OK)
async def main() -> dict:
    '''displaying developer information'''
    return {
        'status': True,
        'dev': 'amirali irvany',
        'url': 't.me/ohmyapi'
    }


parameters: list = [{'item': 'url', 'item': 'timeout'}]
@app.get('/rubino', status_code=status.HTTP_200_OK)
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
    result: dict = rubino(url=url, timeout=timeout)
    return {
        'status': True,
        'dev': 'amirali irvany',
        'url': 't.me/ohmyapi',
        'result': result
    }


parameters: list = [{'item': 'text'}]
@app.get('/font', status_code=status.HTTP_200_OK)
async def font_generate(text: str) -> dict:
    '''This function is for generating fonts. Currently only English language is supported
    :param text:
        The text you want the font to be applied to
    '''
    result: list = font(text=text)
    return {
        'status': True,
        'dev': 'amirali irvany',
        'url': 't.me/ohmyapi',
        'result': result
    }


parameters: list = [{'item': 'text'}]
@app.get('/lang', status_code=status.HTTP_200_OK)
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
        'url': 't.me/ohmyapi',
        'result': result
    }


parameters: list = [{'item': 'content', 'item': 'count', 'item': 'lang'}]
@app.get('/fake', status_code=status.HTTP_200_OK)
async def main(content: str = 'text', count: int = 10, lang: str = 'en_US') -> dict:
    MAX_COUNT_DATA: int = 999
    if count > MAX_COUNT_DATA:
        return {
            'err_message': f'It is not possible to provide more than {MAX_COUNT_DATA} data'
        }

    result = faker_data(content=content, count=count, lang=lang)
    return {
        'status': True,
        'dev': 'amirali irvany',
        'url': 't.me/ohmyapi',
        'result': result
    }
