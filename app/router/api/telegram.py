from fastapi import APIRouter, Response, status

from bs4 import BeautifulSoup

from httpx import AsyncClient, codes

client = AsyncClient()

router = APIRouter(tags=["Rubika Info"])

replaces: dict = {
    "https://t.me/": "https://telegram.me/",
    "t.me/": "https://telegram.me/",
    "@": "https://telegram.me/",
    "https://telegram.me/": "https://telegram.me/",
    "telegram.me/": "https://telegram.me/"
}


@router.get("/tg-info", status_code=status.HTTP_200_OK)
@router.post("/tg-info", status_code=status.HTTP_200_OK)
async def telegram_info(response: Response, query: str) -> dict:
    """
    Web Service to get telegram users information
    """
    url_count = 0
    for start in list(replaces):
        if query.count(start) != 0:
            url_count = 1
            break

    if url_count != 1:
        return {
            "success": False,
            "data": None,
            "error_message": "`url` invalid. (url doesn't have `t.me`, `@` and . . .)"
        }

    for replace in replaces:
        old_text = replace
        new_text = replaces[replace]
        url = query.replace(old_text, new_text)
        if url != query:
            if len(url) < 25:
                return {
                    "success": False,
                    "data": None,
                    "error_message": "`url` invalid. (username is lower than 5 chars.)"
                }

            request = await client.request(method="GET", url=url)
            if request.status_code != codes.OK:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {
                    "success": False,
                    "data": None,
                    "error_message": "A problem has occurred on our end"
                }

            result = dict()
            page = BeautifulSoup(request.text, "html.parser")
            result["profile"] = page.find("meta", property="og:image").attrs["content"]
            result["title"] = page.find("div", {"class": "tgme_page_title"}).text.replace("\n", "")
            result["extra"] = page.find("div", {"class": "tgme_page_extra"}).text.replace("\n", "")
            result["description"] = page.find("div", {"class": "tgme_page_description"})

            if not result["description"]:
                result["description"] = None
            else:
                result["description"] = result["description"].get_text("\n")

            return {
                "success": True,
                "data": result,
                "error_message": None
            }
