from fastapi import APIRouter, Response, status
from fastapi.responses import FileResponse

import pyttsx3

engine = pyttsx3.init()

router = APIRouter(prefix='/api', tags=['Text to voice'])


@router.get('/text2voice', status_code=status.HTTP_200_OK)
@router.post('/text2voice', status_code=status.HTTP_200_OK)
async def text_to_voice(responce: Response, text: str) -> "FileResponse":
    '''Convert text to voice (without artificial intelligence)'''
    FILE_PATH = '/tmp/.heroapi/speech.mp3'
    engine.save_to_file(text=text, filename=FILE_PATH)
    engine.runAndWait()
    return FileResponse(FILE_PATH)
