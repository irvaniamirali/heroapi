from fastapi import FastAPI, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html

from app.router import router

app = FastAPI(
    title="HeroAPI",
    description="Free and open source api",
    contact={
        "name": "HeroTeam",
        "url": "https://github.com/irvaniamirali/HeroAPI",
        "email": "irvaniamirali@proton.me",
    },
    terms_of_service="https://t.me/HeroAPI",
    license_info={
        "name": "Released under MIT LICENSE",
        "identifier": "https://spdx.org/licenses/MIT.html"
    },
    docs_url=None,
    redoc_url=None,
)

templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    """
    Return swagger API document
    """
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="HeroAPI",
        swagger_favicon_url="static/favicon.png",
    )


@app.exception_handler(status.HTTP_404_NOT_FOUND)
async def custom_404_handler(request: Request, __):
    return templates.TemplateResponse(
        "404.html", {
            "request": request
        }
    )


@app.get("/helloworld", status_code=status.HTTP_200_OK)
async def hello_world() -> dict:
    return {
        "success": True,
        "data": "Hello World!"
    }


if __name__ == "app.main":
    app.include_router(router)
