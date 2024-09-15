from fastapi import APIRouter, Response, status

from app.api.sources.base64_api import b64encode, b64decode

router = APIRouter(prefix="/api", tags=["Base64"])


@router.get("/bs64encode", status_code=status.HTTP_200_OK)
@router.post("/bs64encode", status_code=status.HTTP_200_OK)
async def base64encode(string: str) -> dict:
    """
    Encode to Base64 format
    """
    return await b64encode(string)


@router.get("/bs64decode", status_code=status.HTTP_200_OK)
@router.post("/bs64decode", status_code=status.HTTP_200_OK)
async def base64_decode(response: Response, string: str) -> dict:
    """
    Decode from Base64 format
    """
    return await b64decode(response, string)
