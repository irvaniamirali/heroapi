from fastapi import APIRouter, status

from app.api.sources.datetime_api import (
    iso_date, solar_date, ad_date, convert_ad_to_jalali, convert_jalali_to_ad
)

from typing import Optional

router = APIRouter(prefix="/api/datetime", tags=["Date & Time"])


@router.get("/solar", status_code=status.HTTP_200_OK)
async def solar_datetime() -> dict:
    """
    Current Jalali date
    """
    return await solar_date()


@router.get("/ad", status_code=status.HTTP_200_OK)
async def ad_datetime() -> dict:
    """
    Current AD date
    """
    return await ad_date()


@router.get("/iso", status_code=status.HTTP_200_OK)
async def iso_date(year: int, month: int, day: int, prefix: Optional[str] = "/") -> dict:
    """
    Return the Jalali date as a string in ISO 8601 format.
    """
    return await iso_date(year, month, day, prefix)


@router.get("/convert-ad", status_code=status.HTTP_200_OK)
async def convert_ad_to_jalali(year: int, month: int, day: int) -> str:
    """
    Convert AD date to Jalali date.
    """
    return await convert_ad_to_jalali(year, month, day)


@router.get("/convert-jalali", status_code=status.HTTP_200_OK)
async def convert_jalali_to_ad(year: int, month: int, day: int) -> str:
    """
    Convert Jalali date to AD date.
    """
    return await convert_jalali_to_ad(year, month, day)
