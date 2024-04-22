from fastapi import APIRouter, Response, status

import requests

router = APIRouter(prefix='/api', tags=['AI'])


@router.get('/gpt', status_code=status.HTTP_200_OK)
@router.post('/gpt', status_code=status.HTTP_200_OK)
async def chat_gpt_model(responce: Response, query: str) -> dict:
    headers = {
        'Host': 'us-central1-chat-for-chatgpt.cloudfunctions.net',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'com.tappz.aichat/1.2.2 iPhone/16.3.1 hw/iPhone12_5',
        'Accept-Language': 'en',
        'Content-Type': 'application/json; charset=UTF-8',
    }
    endpoint = 'https://us-central1-chat-for-chatgpt.cloudfunctions.net/basicUserRequestBeta'
    data = {
        'data': {
            'message': 'hello, whats your name? ',
        },
    }
    response = requests.post(endpoint, json=data, headers=headers)
    return {
        'success': True,
        'data': response.text
    }
