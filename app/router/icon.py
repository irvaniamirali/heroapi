from fastapi import APIRouter, Response, status

from typing import Optional
import requests
import bs4

router = APIRouter(prefix='/api', tags=['Icon Search'])


@router.get('/icon', tags=['Icon'], status_code=status.HTTP_200_OK)
@router.post('/icon', tags=['Icon'], status_code=status.HTTP_200_OK)
async def icon(responce: Response, query: str, page: Optional[int] = 1) -> dict:
    '''Get the icon from icon-icons.com'''
    request = requests.request(
        method='GET', url=f'https://icon-icons.com/search/icons/?filtro={query}&page={page}'
    )
    if request.status_code != requests.codes.ok:
        responce.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'success': False, 'error_message': 'A problem has occurred on our end'
        }

    soup = bs4.BeautifulSoup(request.text, 'html.parser')
    icons = soup.find_all('div', class_='icon-preview')

    search_result = list()
    for icon in icons:
        data_original = icon.find('img', class_='lazy', src=True)
        search_result.append(data_original['data-original'])

    return {
        'success': True,
        'data': search_result
    }
