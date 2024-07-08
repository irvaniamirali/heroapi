from fastapi import APIRouter, status

from typing import Optional

import wikipediaapi

router = APIRouter(prefix="/api/wikipedia", tags=["Wikipedia Search"])


@router.get("/search", status_code=status.HTTP_200_OK)
@router.post("/search", status_code=status.HTTP_200_OK)
async def wikipedia_search(query: str, results: Optional[int] = 10, lang: Optional[str] = "en"):
    """
    Do a Wikipedia search for `query`.
    """
    wiki = wikipediaapi.Wikipedia("HeroAPI (username@example.com)", lang)
    page = wiki.page(title=query)
    return {
        "success": True,
        "data": {
            "exists": page.exists(),
            "title": page.title,
            "summary": page.summary,
            "text": page.text,
            "language": page.language,
        }
    }
