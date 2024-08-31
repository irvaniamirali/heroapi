from fastapi import APIRouter, status

from app.api.sources.v2ray_api import v2ray

router = APIRouter(prefix="/api", tags=["V2ray Free config"])


@router.get("/v2ray", status_code=status.HTTP_200_OK)
@router.post("/v2ray", status_code=status.HTTP_200_OK)
async def v2ray_config(count: str) -> dict:
    """
    Get free v2ray configs (any types
    """
    return await v2ray(count)
