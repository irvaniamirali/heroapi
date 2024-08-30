from fastapi import APIRouter, Response, status

from app.api.sources.ai import gpt_api


router = APIRouter(prefix="/api", tags=["AI"])


@router.get("/gpt", summary="GPT 3.5", status_code=status.HTTP_200_OK)
@router.post("/gpt", summary="GPT 3.5", status_code=status.HTTP_200_OK)
async def gpt(response: Response, query: str) -> dict:
    """
    ChatGPT 3.5 API.
    """
    return await gpt_api(response, query)
