from fastapi import APIRouter, Response, status

import requests
import bs4

router = APIRouter(prefix='/api', tags=['Food'])


@router.get('/food/v1', status_code=status.HTTP_200_OK)
@router.post('/food/v1', status_code=status.HTTP_200_OK)
async def dictionary(responce: Response, query: str) -> dict:
    '''Search words in deh khoda dictionary'''
    base_url = 'https://mamifood.org'
    request = requests.request(
        method='GET', url=base_url + f'/cooking-training/search/{query}'
    )
    if request.status_code != requests.codes.ok:
        responce.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'success': False, 'error_message': 'A problem has occurred on our end'
        }

    soup = bs4.BeautifulSoup(request.text, 'html.parser')
    articles = soup.find_all('article', id='Table', class_='box m-box col3')

    final_values = list()
    for article in articles:
        image_box = article.find('img', class_='box-img')
        post_info = article.find('a', id='lnkimg', class_='a-img-box')
        post_date = article.find('div', id='Date', class_='inline-block').text

        image_url = base_url + image_box.get('src')
        post_url = post_info.get('href')
        food_title = image_box.get('title')
        final_values.append(
            dict(image_url=image_url, post_url=post_url, food_title=food_title, post_date=post_date)
        )

    return {
        'success': True,
        'data': final_values
    }
