'''this is `ohmyapi`, free and open-source api'''

from fastapi import FastAPI, status
from api.api import *


app = FastAPI()

@app.get('/', status_code=status.HTTP_200_OK)
async def main() -> dict:
    '''This function is for displaying developer information'''
    return {
        'status': True,
        'dev': 'amirali irvany',
        'url': 't.me/ohmyapi'
    }


parameters: list = [{'item': 'url', 'item': 'timeout'}]
@app.get('/rubino', status_code=status.HTTP_200_OK)
async def rubino_dl(url: str, timeout: float = 10) -> dict:
    '''Powered by the myrino library. github > github.com/metect/myrino'''
    result: dict = rubino(url=url, timeout=timeout)
    return {
        'status': True,
        'dev': 'amirali irvany',
        'url': 't.me/ohmyapi',
        'result': result
    }


parameters: list = [{'item': 'text'}]
@app.get('/font', status_code=status.HTTP_200_OK)
async def main(text: str) -> dict:
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
    '''Powered by the `langdetetc` library'''
    result: str = lang(text=text)
    print(result)
    return {
        'status': True,
        'dev': 'amirali irvany',
        'url': 't.me/ohmyapi',
        'result': result
    }
