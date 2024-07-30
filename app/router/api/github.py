from fastapi import APIRouter, Response, status

from typing import Optional

import httpx

client = httpx.AsyncClient()

router = APIRouter(prefix="/github", tags=["GitHub"])

base_url = "https://api.github.com/search/"


async def github_search(path):
    """
    Make asynchronous to GitHub API
    """
    headers: dict = {
        "Accept": "application/vnd.github+json"
    }
    response = await client.request(method="GET", url=path, headers=headers)
    return response


@router.get("/topic", status_code=status.HTTP_200_OK)
@router.post("/topic", status_code=status.HTTP_200_OK)
async def github_topic_search(
        response: Response,
        query: str,
        per_page: Optional[int] = 30,
        page: Optional[int] = 1
) -> dict:
    """
    GitHub topic search web service
    """
    path = base_url + "topics?q=%s&per_page=%s&page=%s" % (query, per_page, page)
    request = await github_search(path=path)
    if request.status_code != httpx.codes.OK:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "data": None,
            "error_message": "A problem has occurred on our end"
        }

    return {
        "success": True,
        "data": request.json(),
        "error_message": None
    }


@router.get("/repo", status_code=status.HTTP_200_OK)
@router.post("/repo", status_code=status.HTTP_200_OK)
async def github_repo_search(
        response: Response,
        name: str,
        sort: Optional[str] = "stars",
        order: Optional[str] = "desc",
        per_page: Optional[int] = 30,
        page: Optional[int] = 1
) -> dict:
    """
    GitHub repository search web service.
    sortlist repository: "stars", "forks", "help-wanted-issues", "updated"
    """
    path = base_url + "repositories?q=%s&s=%s&order=%s&per_page=%s&page=%s"
    request = await github_search(path=path % (name, sort, order, per_page, page))
    if request.status_code != httpx.codes.OK:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "data": None,
            "error_message": "A problem has occurred on our end",
        }

    return {
        "success": True,
        "data": request.json()
    }


@router.get("/users", status_code=status.HTTP_200_OK)
@router.post("/users", status_code=status.HTTP_200_OK)
async def github_users_search(
        response: Response,
        query: str,
        sort: Optional[str] = "followers",
        order: Optional[str] = "desc",
        per_page: Optional[int] = 30,
        page: Optional[int] = 1,
) -> dict:
    """
    GitHub users search web service.
    sortlist repository: "followers", "repositories", "joined"
    """
    path = base_url + "users?q=%s&sort=%s&order=%s&per_page=%s&page=%s"
    request = await github_search(path=path % (query, sort, order, per_page, page))
    if request.status_code != httpx.codes.OK:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "data": None,
            "error_message": "A problem has occurred on our end"
        }

    return {
        "success": True,
        "data": request.json()
    }
