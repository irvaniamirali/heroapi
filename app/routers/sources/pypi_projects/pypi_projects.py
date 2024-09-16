from fastapi import APIRouter, status

from app.api.sources.pypi_projects import package_search

router = APIRouter(prefix="/api", tags=["PyPi projects search"])


@router.get("/pypi", status_code=status.HTTP_200_OK)
@router.post("/pypi", status_code=status.HTTP_200_OK)
async def pypi_projects_search(query: str) -> list:
    """
    PyPi package search web service
    """
    return await package_search(query)
