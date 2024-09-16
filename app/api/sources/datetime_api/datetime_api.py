from persiantools.jdatetime import JalaliDate, JalaliDateTime
from datetime import date, datetime


async def iso_date(year, month, day, prefix):
    date_result = JalaliDate(year, month, day).isoformat()
    if prefix:
        date_result = JalaliDate(year, month, day).strftime(f"%Y{prefix}%m{prefix}%d")
    return date_result


async def solar_date():
    """
    Current Jalali date
    """
    current_date = JalaliDateTime.now()
    return {
        "current": str(current_date.now()),
        "time": {
            "full": current_date.time(),
            "hour": current_date.hour,
            "minute": current_date.minute,
            "second": current_date.second,
            "microsecond": current_date.microsecond
        },
        "date": {
            "full": str(current_date.date()),
            "day": current_date.day,
            "month": current_date.month,
            "year": current_date.year,
        }
    }


async def ad_date():
    """
    Current AD date
    """
    current_date = datetime.now()
    return {
        "current": current_date,
        "time": {
            "full": current_date.time(),
            "hour": current_date.hour,
            "minute": current_date.minute,
            "second": current_date.second,
            "microsecond": current_date.microsecond
        },
        "date": {
            "full": current_date.date(),
            "day": current_date.day,
            "month": current_date.month,
            "year": current_date.year,
        }
    }


async def convert_ad_to_jalali(year, month, day):
    date_result = JalaliDate(date(year, month, day))
    return {"date_result": date_result}


async def convert_jalali_to_ad(year, month, day):
    date_result = JalaliDate.to_jalali(year, month, day)
    return {"date_result": date_result}
