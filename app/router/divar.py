from fastapi import APIRouter, status

from typing import Optional

from ast import literal_eval
import requests

router = APIRouter(prefix='/api', tags=['Shop'])


@router.get('/divar', status_code=status.HTTP_200_OK)
@router.post('/divar', status_code=status.HTTP_200_OK)
async def divar(query: str, city: Optional[str] = 'tehran') -> dict:
    '''Web search service in [Divar](https://divar.ir)'''
    request = requests.post(url=f'https://divar.ir/s/{city}?q={query}').text
    start, finish = request.rfind('['), request.rfind(']')

    values = str()
    computed_value = list(request)[start:finish]
    for index in range(len(computed_value)):
        values += computed_value[index]

    values += ']'
    final_values = literal_eval(node_or_string=values)
    return {
        'success': True,
        'data': final_values
    }
