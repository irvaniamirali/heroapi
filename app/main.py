from fastapi import FastAPI, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html

from app.router.router import routers

app = FastAPI(
    title='HeroAPI',
    description='Free and open source api',
    contact={
        'name': 'HeroTeam',
        'url': 'https://github.com/Hero-API',
        'email': 'dev.amirali.irvany@gmail.com',
    },
    terms_of_service='https://t.me/HeroAPI',
    license_info={
        'name': 'Released under MIT LICENSE',
        'url': 'https://spdx.org/licenses/MIT.html'
    },
    docs_url=None,
    redoc_url=None
)

templates = Jinja2Templates(directory='app/templates')
app.mount('/app/static', StaticFiles(directory='app/static'), name='static')

@app.get('/docs', include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url='/openapi.json',
        title='HeroAPI',
        swagger_favicon_url='app/static/favicon.ico',
    )

@app.exception_handler(status.HTTP_404_NOT_FOUND)
async def custom_404_handler(request: Request, __):
    return templates.TemplateResponse(
        '404.html', {
            'request': request
        }
    )

URLS = [
    'app.router.bardai.router',
    'app.router.art.router',
    'app.router.datetime.router',
    'app.router.fake.router',
    'app.router.language.router',
    'app.router.location.router',
    'app.router.news.router',
    'app.router.music.router',
    'app.router.translate.router',
]

initialize_routers = routers(app, URLS)

if __name__ == 'app.main':
    initialize_routers()

