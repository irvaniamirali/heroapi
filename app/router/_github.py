from fastapi import APIRouter, Response, status

from typing import Optional
import requests

router = APIRouter(prefix='/api', tags=['Github'])

base_url = 'https://api.github.com/search/'
headers = {
    'Accept': 'application/vnd.github+json'
}


@router.get('/github-topic-search', status_code=status.HTTP_200_OK)
@router.post('/github-topic-search', status_code=status.HTTP_200_OK)
async def github_topic_search(
        responce: Response,
        query: str,
        per_page: Optional[int] = 30,
        page: Optional[int] = 1
) -> dict:
    '''Github topic search web service'''
    query_url = 'topics?q=%s&per_page=%s&page=%s'
    request = requests.request(method='GET', url=query_url % (query, per_page, page), headers=headers)
    if request.status_code != requests.codes.ok:
        responce.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'success': False,
            'error_message': 'A problem has occurred on our end'
        }

    return {
        'success': True,
        'data': request.json()
    }


@router.get('/github-repo-search', status_code=status.HTTP_200_OK)
@router.post('/github-repo-search', status_code=status.HTTP_200_OK)
async def github_repo_search(
        responce: Response,
        name: str,
        sort: Optional[str] = 'stars',
        order: Optional[str] = 'desc',
        per_page: Optional[int] = 30,
        page: Optional[int] = 1
) -> dict:
    '''Github repository search web service.
    sortlist repository: "stars", "forks", "help-wanted-issues", "updated"
    '''
    query_url = base_url + 'repositories?q=%s&s=%s&order=%s&per_page=%s&page=%s'
    request = requests.request(
        method='POST', url=query_url % (name, sort, order, per_page, page), headers=headers
    )
    if request.status_code != requests.codes.ok:
        responce.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'success': False,
            'error_message': 'A problem has occurred on our end'
        }


    return {
        'success': True,
        'data': request.json()
    }


@router.get('/github-users-search', status_code=status.HTTP_200_OK)
@router.post('/github-users-search', status_code=status.HTTP_200_OK)
async def github_users_search(
        responce: Response,
        query: str,
        sort: Optional[str] = 'followers',
        order: Optional[str] = 'desc',
        per_page: Optional[int] = 30,
        page: Optional[int] = 1,
) -> dict:
    '''Github users search web service.
    sortlist repository: "followers", "repositories", "joined"
    '''
    query_url = base_url + 'users?q=%s&sort=%s&order=%s&per_page=%s&page=%s'
    request = requests.request(
        method='POST', url=query_url % (query, sort, order, per_page, page), headers=headers
    )
    if request.status_code != requests.codes.ok:
        responce.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'success': False,
            'error_message': 'A problem has occurred on our end'
        }

    return {
        'success': True,
        'data': request.json()
    }
