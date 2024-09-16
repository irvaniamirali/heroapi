from httpx import AsyncClient

client = AsyncClient()

BASE_URL = "https://api.github.com/search/"

HEADERS = {
    "Accept": "application/vnd.github+json"
}


async def http_request(path):
    """
    Execute asynchronous request to GitHub API
    """
    response = await client.request(method="GET", url=path, headers=HEADERS)
    return response


async def topic_search(query, per_page, page):
    path = BASE_URL + "topics?q=%s&per_page=%s&page=%s" % (query, per_page, page)
    response = await http_request(path=path)
    return response.json()


async def repo_search(name, sort, order, per_page, page):
    path = BASE_URL + "repositories?q=%s&s=%s&order=%s&per_page=%s&page=%s"
    response = await http_request(path=path % (name, sort, order, per_page, page))
    return response.json()


async def users_search(query, sort, order, per_page, page):
    path = BASE_URL + "users?q=%s&sort=%s&order=%s&per_page=%s&page=%s"
    response = await http_request(path=path % (query, sort, order, per_page, page))
    return response.json()
