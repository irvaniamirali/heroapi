from fastapi import FastAPI, Request, status
from fastapi.templating import Jinja2Templates
from .api.api import HeroAPI

heroapi = HeroAPI()


app = FastAPI()
templates = Jinja2Templates(directory='app/templates')


@app.exception_handler(404)
async def custom_404_handler(request: Request, __) -> 'template page':
    return templates.TemplateResponse(
        '404.html', {
            'request': request
        }
    )


@app.get('/', status_code=status.HTTP_200_OK)
async def main() -> dict:
    '''displaying developer information
    :return
        status, developer name and ...
    '''
    return await heroapi.main_app()


parameters: list = [{'item': 'auth', 'item': 'url', 'item': 'timeout'}]
@app.get('/api/rubino', status_code=status.HTTP_200_OK)
@app.post('/api/rubino', status_code=status.HTTP_200_OK)
async def rubino(auth: str, url: str, timeout: float = 10) -> dict:
    '''This api is used to get the information of the post(s) in Rubino Messenger
    :param url:
        The link of the desired post. Example: `https://rubika.ir/post/xxxxxx`
    :param timeout:
        For manage timeout when the rubika server
    :return:
        Full post information

    If you want more details, go to this address: https://github.com/metect/myrino
    '''
    return await heroapi.rubino(auth=auth, url=url, timeout=timeout)


parameters: list = [{'item': 'text'}]
@app.get('/api/font', status_code=status.HTTP_200_OK)
@app.post('/api/font', status_code=status.HTTP_200_OK)
async def font(text: str = 'Heroapi') -> dict:
    '''This function is for generating fonts. Currently only English language is supported
    :param text:
        The text you want the font to be applied to
    '''
    try:
        return await heroapi.font_generate(text=text)
    except IndexError:
        return await heroapi.execute(
            status=False,
            err_message='Currently, Persian language is not supported'
        )


parameters: list = [{'item': 'text'}]
@app.get('/api/lang', status_code=status.HTTP_200_OK)
@app.post('/api/lang', status_code=status.HTTP_200_OK)
async def lang_detect(text: str) -> dict:
    '''This function is to identify the language of a text
    :param text:
        Your desired text
    :return:
        example: `en` or `fa`

    Powered by the `langdetetc` library
    '''
    return await heroapi.lang(text=text)


parameters: list = [{'item': 'text', 'item': 'to_lang', 'item': 'from_lang'}]
@app.get('/api/translate', status_code=status.HTTP_200_OK)
@app.post('/api/translate', status_code=status.HTTP_200_OK)
async def translate(text: str, to_lang: str = 'auto', from_lang: str = 'auto') -> dict:
    '''This API, which is based on the Google Translate API, is used to translate texts'''
    return await heroapi.translator(text=text, to_lang=to_lang, from_lang=from_lang)


parameters: list = [{'item': 'count', 'item': 'lang'}]
@app.get('/api/faketext', status_code=status.HTTP_200_OK)
@app.post('/api/faketext', status_code=status.HTTP_200_OK)
async def fake_text(count: int = 100, lang: str = 'en_US') -> dict:
    '''This api is used to generate fake text
    :param count
        Number of words, example >>> `10`
    :param lang
        desired language, example >>> `en_US` or `fa_IR`

    Power taken from the library `Faker`
    '''
    return await heroapi._faketext(count=count, lang=lang)


@app.get('/api/datetime', status_code=status.HTTP_200_OK)
@app.post('/api/datetime', status_code=status.HTTP_200_OK)
async def datetime() -> dict:
    '''This api is used to display date and time in solar'''
    return await heroapi.date_time()


@app.get('/api/usd', status_code=status.HTTP_200_OK)
@app.post('/api/usd', status_code=status.HTTP_200_OK)
async def usd() -> dict:
    '''api to get live currency prices from the `https://irarz.com` website'''
    return await heroapi.usd()
