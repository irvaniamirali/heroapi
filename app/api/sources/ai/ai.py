from httpx import AsyncClient

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
    "Origin": "https://chat18.aichatos8.com",
    "Access-Control-Allow-Origin": "*"
}

PAYLOAD = {
    "prompt": None,
    "userId": "#/chat/1724442116057",
    "network": True,
    "system": "",
    "withoutContext": False,
    "stream": False
}


async def gpt(query):
    """
    ChatGPT 3.5 API
    """
    PAYLOAD["prompt"] = query
    HEADERS["User-Agent"] = user_agent.generate_user_agent()
    response = await client.post(HOST, json=PAYLOAD, headers=HEADERS)
    response.raise_for_status()
    return {"model": "GPT-4", "origin": query, "message": response.text}
