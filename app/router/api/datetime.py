from fastapi import APIRouter, Response, status

from typing import Optional
import jdatetime
import datetime

router = APIRouter(prefix='/api', tags=['Date & time'])


@router.get('/datetime', status_code=status.HTTP_200_OK)
@router.post('/datetime', status_code=status.HTTP_200_OK)
async def date_time(responce: Response) -> dict:
    '''Date and time display web service'''
    now_datatime = datetime.datetime.now()
    current_date = now_datatime.strftime('%a, %d %b %Y %H:%M:%S')
    return {
        'success': True,
        'data': current_date
    }


@router.get('/convert-date', status_code=status.HTTP_200_OK)
@router.post('/convert-date', status_code=status.HTTP_200_OK)
async def convert_date(day: int, month: int, year: int) -> dict:
    '''Convert Shamsi date to Gregorian'''
    result_date = jdatetime(day=day, month=month, year=year).togregorian()
    return {
        'success': True,
        'data': result_date
    }
