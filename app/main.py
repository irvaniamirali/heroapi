from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from httpx import HTTPStatusError

from app.routers import Routers, paths
from app.settings.config import app_config, middleware_config

app = FastAPI(**app_config)

# add CORS middleware to the app
app.add_middleware(CORSMiddleware, **middleware_config)

templates = Jinja2Templates(directory="app/templates")

# mount the static files path
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.exception_handler(HTTPStatusError)
async def handle_api_error(_: Request, exc: HTTPStatusError) -> JSONResponse:
    """
    Handle API errors.
    """
    # TODO: make specific error messages for each error code
    message = {"error_message": "A problem has occurred on our end."}
    return JSONResponse(status_code=exc.response.status_code, content=message)


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    """
    Handle HTTP exceptions.
    """
    # dummy handler for now. Maybe we'll add more handlers later.
    if not isinstance(exc.detail, dict):
        exc.detail = {"detail": exc.detail}
    if not exc.detail.get("status"):
        # The same 'status' key is used in the API error 'to_dict' method.
        exc.detail["status"] = exc.status_code
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


@app.exception_handler(status.HTTP_404_NOT_FOUND)
async def custom_404_handler(request: Request, _):
    """
    Handle 404 page (Not found)
    """
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
