from fastapi import APIRouter, Response, status

from typing import Optional

from jalali.Jalalian import jdate
import jdatetime

router = APIRouter(prefix="/api", tags=["Date & time"])


@router.get("/datetime", status_code=status.HTTP_200_OK)
@router.post("/datetime", status_code=status.HTTP_200_OK)
async def date_time(responce: Response, number_lang: str = "fa") -> dict:
    """
    Date and time display web service
    """
    current_date = jdate("H:i:s ,Y/n/j", tr_num=number_lang)
    return {
        "success": True,
        "data": current_date
    }


@router.get("/convert-date", status_code=status.HTTP_200_OK)
@router.post("/convert-date", status_code=status.HTTP_200_OK)
async def convert_date(day: int, month: int, year: int) -> dict:
    """
    Convert Shamsi date to Gregorian
    """
    result_date = jdatetime.date(day=day, month=month, year=year).togregorian()
    return {
        "success": True,
        "data": result_date
    }
