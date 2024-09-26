from fastapi import APIRouter, Query, status

from typing import Optional, Annotated

from app.api.sources.faker import name, email, text

router = APIRouter(prefix="/api/faker", tags=["Fake data"])


@router.get("/text", status_code=status.HTTP_200_OK)
async def faker_text(language: Optional[str] = "en") -> dict:
    """
    Random fake text API
    :language: Only `en` and `fa` are available.
    """
    return await text(language)


@router.get("/name", status_code=status.HTTP_200_OK)
async def faker_name(count: Annotated[int | None, Query(lt=999)] = 20, language: Optional[str] = "en") -> list:
    """
    Random fake name API
    :language: Only `en` and `fa` are available.
    """
    return await name(count, language)


@router.get("/email", status_code=status.HTTP_200_OK)
async def faker_email(count: Annotated[int | None, Query(lt=999)] = 20) -> list:
    """
    Random fake email API
    """
    return await email(count)
