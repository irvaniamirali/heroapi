from fastapi import APIRouter, Response, status

from typing import Optional
import langdetect
import json

router = APIRouter(prefix='/api', tags=['Art'])


@router.get('/font', status_code=status.HTTP_200_OK)
@router.post('/font', status_code=status.HTTP_200_OK)
async def font(responce: Response, text: Optional[str] = 'HeroAPI') -> dict:
    '''Generate ascii fonts. Currently only English language is supported'''
    if langdetect.detect(text) in ['fa', 'ar', 'ur']:
        responce.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'success': False, 'error_message': 'Currently, Persian language is not supported'
        }
    else:
        with open('app/jsonfiles/font.json', 'r') as f:
            fonts = json.load(f)

        converted_text = str()
        for count in range(0, len(fonts)):
            for char in text:
                if char.isalpha():
                    char_index = ord(char.lower()) - 97
                    converted_text += fonts[str(count)][char_index]
                else:
                    converted_text += char

            converted_text += '\n'
            final_values: list = converted_text.split('\n')[0:-1]

        return {
            'success': True,
            'data': final_values
        }
