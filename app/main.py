from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.openapi.docs import get_swagger_ui_html

from contextlib import asynccontextmanager

from app.router.router import Routers

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.in_flight_requests_count = 0
    yield


docs_url, redoc_url = None, None

app = FastAPI(
    title='HeroAPI',
    description='Free and open source api',
    contact={
        'name': 'HeroTeam',
        'url': 'https://github.com/irvanyamirali/HeroAPI',
        'email': 'irvanyamirali@gmail.com',
    },
    terms_of_service='https://t.me/HeroAPI',
    license_info={
        'name': 'Released under MIT LICENSE',
        'identifier': 'https://spdx.org/licenses/MIT.html'
    },
    lifespan=lifespan,
    docs_url=docs_url,
    redoc_url=redoc_url,
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

@app.middleware('http')
async def in_flight_requests_counter(request, call_next):
    app.state.in_flight_requests_count += 1
    return await call_next(request)


URLS: list = [
    'app.router.api.art.router',
    'app.router.api._base64.router',
    'app.router.api.datetime.router',
    'app.router.api.dictionary.router',
    'app.router.api.fake.router',
    'app.router.api._github.router',
    'app.router.api.location.router',
    'app.router.api.news.router',
    'app.router.api.music.router',
    'app.router.api.pypi.router',
    'app.router.api.store.router',
    'app.router.api.rubino.router',
    'app.router.api.translate.router',
    'app.router.api.other.router',
]

initialize_routers = Routers(app, URLS)

if __name__ == 'app.main':
    initialize_routers()
