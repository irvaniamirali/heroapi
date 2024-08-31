from fastapi import status
from httpx import AsyncClient, codes

import user_agent

client = AsyncClient()

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

PAYLOAD = {
    "prompt": None,
    "userId": "#/chat/1724442116057",
    "network": True,
    "system": "",
    "withoutContext": False,
    "stream": False
}


async def gpt(response, query):
    """
    ChatGPT 3.5 API
    """
    PAYLOAD["prompt"] = query
    HEADERS["User-Agent"] = user_agent.generate_user_agent()
    query_response = await client.post(HOST, json=PAYLOAD, headers=HEADERS)
    if query_response.status_code != codes.OK:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "data": None,
            "error_message": "A problem has occurred on our end"
        }

    return {
        "success": True,
        "data": {
            "message": query_response.text,
            "origin": query,
            "model": "GPT-3.5",
        },
        "error_message": None
    }
