from fastapi import APIRouter, Response, status

import codecs
import base64

router = APIRouter(prefix='/api', tags=['Base64'])


@router.get('/bs64encode', status_code=status.HTTP_200_OK)
@router.post('/bs64encode', status_code=status.HTTP_200_OK)
async def base64encode(text: str) -> dict:
    b_string = codecs.encode(text, 'utf-8')
    output = base64.b64encode(b_string)
    return {
        'success': True,
        'data': output
    }


@router.get('/bs64decode', status_code=status.HTTP_200_OK)
@router.post('/bs64decode', status_code=status.HTTP_200_OK)
async def b64encode(responce: Response, text: str) -> dict:
    b_string = codecs.encode(text, 'utf-8')
    try:
        output = base64.b64decode(b_string)
        return {
            'success': True,
            'data': output
        }
    except:
        responce.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'success': False, 'error_message': 'This text not base64'
        }
