from fastapi import APIRouter, status

from typing import Optional

from app.api.sources.others_api import convert_html_to_json_api

router = APIRouter(prefix="/api")


@router.get("/html2json", tags=["Convert HTML to JSON"], status_code=status.HTTP_200_OK)
async def convert_html_to_json(
        html: str,
        capture_element_values: Optional[bool] = True,
        capture_element_attributes: Optional[bool] = True
) -> dict:
    """
    Convert HTML document to json
    """
    return await convert_html_to_json_api(html, capture_element_values, capture_element_attributes)
