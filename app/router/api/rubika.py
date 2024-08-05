from fastapi import APIRouter, Response, status

from bs4 import BeautifulSoup

from httpx import AsyncClient, codes

client = AsyncClient()

router = APIRouter(tags=["Rubika Info"])


@router.get("/rubika-info", status_code=status.HTTP_200_OK)
@router.post("/rubika-info", status_code=status.HTTP_200_OK)
async def rubika_info(response: Response, username: str) -> dict:
    """
    Web Service to get rubika users information
    """
    result = dict()
    request = await client.request(
        method="GET", url=f"https://rubika.ir/{username}"
    )
    if request.status_code != codes.OK:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "data": None,
            "error_message": "A problem has occurred on our end"
        }

    bs4 = BeautifulSoup(request.text, "html.parser")
    if bs4.head.title.text == "Rubika":
        try:
            profile = bs4.find("img", {"class": "dialog-avatar"})
            result["profile"] = profile.attrs["src"]
        except AttributeError:
            result["profile"] = None

        title = bs4.find("div", {"class": "l-title"})
        result["title"] = title.text
        try:
            description = bs4.find("div", {"class": "l-desc"})
            result["description"] = description.text
        except AttributeError:
            result["description"] = None

        member_count = int(bs4.find("span", {"class": "user-last-message"}).text.replace(" مشترک ", ""))
        result["member_count"] = member_count
        return {
            "success": True,
            "data": result,
            "error_message": None
        }
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "success": False,
            "data": result,
            "error_message": "ID not found."
        }
