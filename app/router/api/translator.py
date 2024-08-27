from fastapi import status

import urllib.parse
import re
import html
import user_agent

from httpx import AsyncClient, codes

client = AsyncClient()

URL = "https://translate.google.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0"
}


async def translate(response, text, to_lang, from_lang):
    HEADERS["User-Agent"] = user_agent.generate_user_agent()
    query_url = f"{URL}/m?tl={to_lang}&sl={from_lang}&q={urllib.parse.quote(text)}"
    request = await client.request(method="GET", url=query_url, headers=HEADERS)
    if request.status_code != codes.OK:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "data": None,
            "error_message": "A problem has occurred on our end"
        }

    translated_text = re.findall(r'(?s)class="(?:t0|result-container)">(.*?)<', request.text)
    return {
        "success": True,
        "data": html.unescape(translated_text[0]),
        "error_message": None
    }
