from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html

from app.settings.config import LiveAPI_docs_url

router = APIRouter()


@router.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    """
    Return swagger API document
    """
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="HeroAPI",
        swagger_favicon_url="static/favicon.png",
    )


@router.get("/liveapi", include_in_schema=False, response_class=RedirectResponse)
async def redirect_live_api_docs():
    """
    Redirect the LiveAPI Docs url
    """
    return RedirectResponse(LiveAPI_docs_url)
