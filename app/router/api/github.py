from httpx import AsyncClient

client = AsyncClient()

BASE_URL = "https://api.github.com/search/"

HEADERS = {
    "Accept": "application/vnd.github+json"
}


async def github_search(path):
    """
    Execute asynchronous request to GitHub API
    """
    response = await client.request(method="GET", url=path, headers=HEADERS)
    return response


async def topic_search(query, per_page, page):
    path = BASE_URL + "topics?q=%s&per_page=%s&page=%s" % (query, per_page, page)
    request = await github_search(path=path)
    return {
        "success": True,
        "data": request.json(),
        "error_message": None
    }


async def repo_search(name, sort, order, per_page, page):
    path = BASE_URL + "repositories?q=%s&s=%s&order=%s&per_page=%s&page=%s"
    request = await github_search(path=path % (name, sort, order, per_page, page))
    return {
        "success": True,
        "data": request.json(),
        "error_message": None
    }


async def users_search(query, sort, order, per_page, page):
    path = BASE_URL + "users?q=%s&sort=%s&order=%s&per_page=%s&page=%s"
    request = await github_search(path=path % (query, sort, order, per_page, page))
    return {
        "success": True,
        "data": request.json(),
        "error_message": None
    }
