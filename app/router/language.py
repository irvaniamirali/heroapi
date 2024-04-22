from fastapi import APIRouter, Response, status

import langdetect

router = APIRouter(prefix='/api', tags=['Language'])


@router.get('/lang', tags=['Language Detect'], status_code=status.HTTP_200_OK)
@router.post('/lang', tags=['Language Detect'], status_code=status.HTTP_200_OK)
async def language_detect(responce: Response, text: str) -> dict:
    '''Identifying the language of texts'''
    try:
        result_detected = langdetect.detect(text)
        return {
            'success': True,
            'data': result_detected
        }
    except langdetect.LangDetectException:
        responce.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'success': False,
            'error_message': 'The value of the `text` parameter is not invalid'
        }
