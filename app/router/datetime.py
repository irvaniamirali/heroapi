from fastapi import APIRouter, status

from jalali.Jalalian import jdate
from jdatetime import date as jdatetime
from typing import Optional


router = APIRouter(prefix='/api', tags=['Date & time'])

@router.get('/datetime', status_code=status.HTTP_200_OK)
@router.post('/datetime', status_code=status.HTTP_200_OK)
async def datetime(tr_num: Optional[str] = 'en') -> dict:
    '''Display detailed information about the date of the solar calendar'''
    current_date = jdate('H:i:s ,Y/n/j', tr_num=tr_num)
    return {
        'success': True,
        'dev': 'Hero-Team',
        'url': 'https://t.me/HeroAPI',
        'github': 'https://github.com/metect/HeroAPI',
        'data': current_date
    }


@router.get('/convert-date', status_code=status.HTTP_200_OK)
@router.post('/convert-date', status_code=status.HTTP_200_OK)
async def convert_date(day: int, month: int, year: int) -> dict:
    '''Convert Shamsi date to Gregorian'''
    result_date = date(day=day, month=month, year=year).togregorian()
    return {
        'success': True,
        'dev': 'Hero-Team',
        'url': 'https://t.me/HeroAPI',
        'github': 'https://github.com/metect/HeroAPI',
        'data': current_date
    }
