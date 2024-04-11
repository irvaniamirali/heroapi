from fastapi import APIRouter, HTTPException, status

from jalali.Jalalian import jdate
from typing import Optional


router = APIRouter(prefix='/api')

@app.get('/datetime', tags=['Date & time'], status_code=status.HTTP_200_OK)
@app.get('/datetime', tags=['Date & time'], status_code=status.HTTP_200_OK)
async def datetime(tr_num: Optional[str] = 'en') -> dict:
    '''Display detailed information about the date of the solar calendar'''
    current_date = jdate('H:i:s ,Y/n/j', tr_num=tr_num)
    return {
        'success': True,
        'dev': 'Hero-Team',
        'url': 'https://t.me/HeroAPI',
        'github': 'https://github.com/Hero-API/HeroAPI',
        'data': current_date
    }
