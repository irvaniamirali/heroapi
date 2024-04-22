from fastapi import APIRouter, Response, status

from typing import Optional
import faker

router = APIRouter(prefix='/api', tags=['Fake data'])


@router.get('/faker', status_code=status.HTTP_200_OK)
@router.post('/faker', status_code=status.HTTP_200_OK)
async def fake_data(
        responce: Response,
        item: Optional[str] = 'text',
        count: Optional[int] = '99',
        lang: Optional[str] = 'en'
) -> dict:
    '''Production fake data. all items: (`text`, `name`, `email`)'''
    if int(count) > 100:
        responce.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'success': False, 'error_message': 'The amount is too big. Send a smaller number `count`'
        }
    else:
        final_values = list()
        if item == 'text':
            return {
                'success': True,
                'data': faker.Faker([lang]).text(count)
            }
        elif item == 'name':
            for i in range(count):
                final_values.append(faker.Faker([lang]).name())

        elif item == 'email':
            for i in range(count):
                final_values.append(faker.Faker([lang]).email())

    return {
        'success': True,
        'data': final_values
    }
