from fastapi import APIRouter, status

from typing import Optional

router = APIRouter(prefix="/api", tags=["Google search"])


@router.get("/google", status_code=status.HTTP_200_OK)
@router.post("/google", status_code=status.HTTP_200_OK)
async def google_search(
        query: str,
        num_results: Optional[int] = 10,
        lang: Optional[str] = "en",
        safe: Optional[str] = "active",
) -> dict:
    """
    Search the Google search engine
    """
    return {
        "success": False,
        "data": None
    }
