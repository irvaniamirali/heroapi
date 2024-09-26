import urllib.parse
import html
import user_agent

from re import findall
from httpx import AsyncClient

client = AsyncClient()

URL = "https://translate.google.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0"
}


async def translate(text, to_lang, from_lang):
    HEADERS["User-Agent"] = user_agent.generate_user_agent()
    query_url = f"{URL}/m?tl={to_lang}&sl={from_lang}&q={urllib.parse.quote(text)}"
    response = await client.request(method="GET", url=query_url, headers=HEADERS)
    response.raise_for_status()

    translated_text = findall(r'(?s)class="(?:t0|result-container)">(.*?)<', response.text)
    return {
        "origin": text,
        "to_lang": to_lang,
        "from_lang": from_lang,
        "text": html.unescape(translated_text[0])
    }
