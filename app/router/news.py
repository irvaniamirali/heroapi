from fastapi import APIRouter, Response, status

from typing import Optional
import requests
import bs4

router = APIRouter(prefix='/api', tags=['News'])

@router.get('/news', status_code=status.HTTP_200_OK)
@router.post('/news', status_code=status.HTTP_200_OK)
async def news(responce: Response, page: Optional[int] = 1) -> dict:
    '''Web service to display news. onnected to the site www.tasnimnews.com'''
    url = 'https://www.tasnimnews.com'
    request = requests.request('GET', f'{url}/fa/top-stories?page={page}')
    if request.status_code != requests.codes.ok:
        responce.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'success': False, 'error_message': 'A problem has occurred on our end'
        }

    soup = bs4.BeautifulSoup(request.text, 'html.parser')
    articles = soup.find_all('article', class_='list-item')

    search_result = list()
    for article in articles:
        title = article.find('h2', class_='title').text.strip()
        description = article.find('h4').text.strip()
        image = article.find('img', src=True)
        full_url = article.find('a', href=True)
        search_result.append(
            dict(
                title=title,
                description=description,
                url=url + full_url['href'],
                image=image['src']
            )
        )

    return {
        'success': True,
        'data': search_result
    }
