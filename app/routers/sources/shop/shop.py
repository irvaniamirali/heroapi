from fastapi import APIRouter, status

from typing import Optional

from app.api.sources.shop import divar

router = APIRouter(prefix="/api", tags=["Divar Products search"])


@router.get("/divar", status_code=status.HTTP_200_OK)
async def divar_products_search(query: str, city: Optional[str] = "tehran") -> list:
    """
    Web search service in [Divar](https://divar.ir).
    """
    return await divar(query, city)
