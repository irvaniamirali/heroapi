from fastapi import APIRouter, status

from app.api.sources.others_api import convert_html_to_json_api

router = APIRouter(prefix="/api")


@router.get("/html2json", tags=["Convert HTML to JSON"], status_code=status.HTTP_200_OK)
@router.post("/html2json", tags=["Convert HTML to JSON"], status_code=status.HTTP_200_OK)
async def convert_html_to_json(html: str) -> dict:
    """
    Convert HTML document to json
    """
    return await convert_html_to_json_api(html)
