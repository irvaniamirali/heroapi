from fastapi import APIRouter, status

from typing import Optional

from app.api.sources.translator import translate as translate_api

router = APIRouter(prefix="/api", tags=["Translate"])


@router.get("/translate", status_code=status.HTTP_200_OK)
async def translate(text: str, to_lang: Optional[str] = "auto", from_lang: Optional[str] = "auto") -> dict:
    """
    Translation of texts based on the Google Translate engine.
    """
    return await translate_api(text, to_lang, from_lang)
