from fastapi import APIRouter, Response, status

from app.router.api import ai

router = APIRouter(prefix="/api")


@router.get("/gpt", status_code=status.HTTP_200_OK)
@router.post("/gpt", status_code=status.HTTP_200_OK)
async def gpt(response: Response, query: str) -> dict:
    """
    ChatGPT 3.5 API
    """
    return await ai.gpt(response, query)
