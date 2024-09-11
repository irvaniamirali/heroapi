from httpx import AsyncClient, codes

from random import randint

client = AsyncClient()

GITHUB_REPO = "https://github.com/barry-far/V2ray-Configs"
RAW_URL = "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt"


async def http_request(url: str, method: str = "GET", max_retry: int = 3):
    """
    Execute asynchronous request to GitHub
    """
    for _ in range(max_retry):
        response = await client.request(method=method, url=url)
        if response.status_code == codes.OK:
            return response.text


async def v2ray(count):
    """
    Get free v2ray configs (any types)
    """
    response = await http_request(RAW_URL)
    configs = response.splitlines()

    for config in configs:
        if config.startswith("#"):
            index = configs.index(config)
            del configs[index]

    if count:
        unique_configs = []
        for config in range(count):
            if config not in configs:
                random_index = randint(0, len(configs))
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
