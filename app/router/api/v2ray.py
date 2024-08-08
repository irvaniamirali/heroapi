from fastapi import APIRouter, status

from typing import Optional

import random
import httpx

client = httpx.AsyncClient()

router = APIRouter(tags=["V2ray config"])


GITHUB_REPO = "https://github.com/barry-far/V2ray-Configs"
URL = "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt"


async def http_request(url: str, method: str = "GET", max_retry: int = 3):
    """
    Execute asynchronous request to GitHub
    """
    for _ in range(max_retry):
        response = await client.request(method=method, url=url)
        if response.status_code == httpx.codes.OK:
            return response.text


@router.get("/v2ray", status_code=status.HTTP_200_OK)
@router.post("/v2ray", status_code=status.HTTP_200_OK)
async def v2ray(num_results: Optional[int] = 10):
    """
    Get free v2ray configs (any types)
    """
    response = await http_request(URL)
    configs = response.splitlines()

    for config in configs:
        if config.startswith("#"):
            index = configs.index(config)
            del configs[index]

    if num_results:
        unique_configs = []
        for config in range(num_results):
            if config not in configs:
                random_index = random.randint(0, len(configs))
                unique_configs.append(configs[random_index])

        return {
            "success": True,
            "data": {
                "configs": unique_configs,
                "count": len(unique_configs),
            },
            "github_repo": GITHUB_REPO,
            "error_message": None
        }

    return {
        "success": True,
        "data": {
            "configs": configs,
            "count": len(configs),
        },
        "github_repo": GITHUB_REPO,
        "error_message": None
    }
