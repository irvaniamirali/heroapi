from fastapi import APIRouter, Response, status

from typing import Optional
import requests


router = APIRouter(prefix='/api', tags=['Domain'])

@router.get('/domain-price', status_code=status.HTTP_200_OK)
@router.post('/domain-price', status_code=status.HTTP_200_OK)
async def domain_price(responce: Response) -> dict:
    '''Get Domain price from [parsvds.com](https://parsvds.com) web site'''
    request = requests.request(method='GET', url=f'https://parsvds.com/domain/')
    if request.status_code != requests.codes.ok:
        responce.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'success': False, 'error_message': 'A problem has occurred on our end'
        }

    soup = bs4.BeautifulSoup(request.text, 'html.parser')
    table_rows = soup.find_all('tr')

    search_result = list()
    for row in table_rows[1:]:
        domain = row.find_all('td')
        price = row.find_all('td')
        search_result.append(
            dict(
                domain=domain[0].text, price=price[1].text
            )
        )

    return {
        'success': True,
        'data': search_result
    }
