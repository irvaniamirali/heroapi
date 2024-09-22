from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers import Routers, paths
from app.settings.config import app_config, middleware_config

app = FastAPI(**app_config)

# add CORS middleware to the app
app.add_middleware(CORSMiddleware, **middleware_config)

templates = Jinja2Templates(directory="app/templates")

# mount the static files path
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.exception_handler(Exception)
async def common_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle API errors.
    """
    # TODO: dummy handler for now. Maybe we'll add more handlers later.
    message = {"error_message": "A problem has occurred on our end."}
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=message)


@app.exception_handler(status.HTTP_404_NOT_FOUND)
async def custom_404_handler(request: Request, exc: Exception):
    """
    Handle 404 page (Not found)
    """
    return templates.TemplateResponse("404.html", {"request": request})


@app.get("/helloworld", status_code=status.HTTP_200_OK)
async def hello_world() -> dict:
    return {
        "success": True,
        "message": "Hello World!"
    }


initialize_routers = Routers(app, paths)

if __name__ == "app.main":
    initialize_routers()
