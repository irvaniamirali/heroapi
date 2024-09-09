from fastapi import FastAPI, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.routers import Routers
from app.routers.paths import paths
from app.settings.config import app_config

app = FastAPI(**app_config)

templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


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

initialize_routers = Routers(app, paths)

if __name__ == "app.main":
    initialize_routers()
