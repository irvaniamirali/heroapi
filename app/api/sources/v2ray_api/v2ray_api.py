from httpx import AsyncClient, codes

from random import randint

client = AsyncClient()

GITHUB_REPO = "https://github.com/barry-far/V2ray-Configs"
RAW_URL = "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt"


async def v2ray(count):
    """
    Get free v2ray configs (any types)
    """
    response = await client.request(method="GET", url=RAW_URL)
    configs = response.text.splitlines()

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

        return {"github_repo": GITHUB_REPO, "count": len(unique_configs), "configs": unique_configs}

    return {"github_repo": GITHUB_REPO, "count": len(configs), "configs": configs}
