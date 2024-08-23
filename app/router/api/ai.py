from fastapi import APIRouter, Response, status

from httpx import AsyncClient, codes

import user_agent

client = AsyncClient()

router = APIRouter(tags=["AI"])

HOST = "https://api.binjie.fun/api/generateStream"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json",
    "Referer": "https://chat18.aichatos8.com/",
    "Origin": "https://chat18.aichatos8.com"

}


@router.get("/gpt", status_code=status.HTTP_200_OK)
@router.post("/gpt", status_code=status.HTTP_200_OK)
async def chat_gpt(response: Response, query: str) -> dict:
    """
    ChatGPT 3.5 API
    """
    data = {
        "prompt": query,
        "userId": "#/chat/1724442116057",
        "network": True,
        "system": "",
        "withoutContext": False,
        "stream": False
    }
    query_response = await client.post(HOST, json=data, headers=HEADERS)
    if query_response.status_code != codes.OK:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "data": None,
            "error_message": "A problem has occurred on our end"
        }

    return {
        "success": True,
        "data": query_response.text,
        "error_message": None
    }
