from fastapi import APIRouter, status

from app.api.sources.github import topic_search, repo_search, users_search

from typing import Optional

router = APIRouter(prefix="/api/github", tags=["GitHub"])


@router.get("/topic", status_code=status.HTTP_200_OK)
@router.post("/topic", status_code=status.HTTP_200_OK)
async def github_topic_search(query: str, per_page: Optional[int] = 30, page: Optional[int] = 1) -> dict:
    """
    GitHub topic search web service
    """
    return await topic_search(query, per_page, page)


@router.get("/repo", status_code=status.HTTP_200_OK)
@router.post("/repo", status_code=status.HTTP_200_OK)
async def github_repo_search(
        name: str,
        sort: Optional[str] = "stars",
        order: Optional[str] = "desc",
        per_page: Optional[int] = 30,
        page: Optional[int] = 1
) -> dict:
    """
    GitHub repository search web service.
    sort list repository: "stars", "forks", "help-wanted-issues", "updated".
    """
    return await repo_search(name, sort, order, per_page, page)


@router.get("/users", status_code=status.HTTP_200_OK)
@router.post("/users", status_code=status.HTTP_200_OK)
async def github_users_search(
        query: str,
        sort: Optional[str] = "followers",
        order: Optional[str] = "desc",
        per_page: Optional[int] = 30,
        page: Optional[int] = 1,
) -> dict:
    """
    GitHub users search web service.
    sort list repository: "followers", "repositories", "joined".
    """
    return await users_search(query, sort, order, per_page, page)
