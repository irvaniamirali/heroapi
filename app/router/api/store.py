from fastapi import APIRouter, Response, status

from ast import literal_eval
from typing import Optional

import httpx

client = httpx.AsyncClient()

router = APIRouter(tags=["Store"])


@router.get("/divar", status_code=status.HTTP_200_OK)
@router.post("/divar", status_code=status.HTTP_200_OK)
async def divar(response: Response, query: str, city: Optional[str] = "tehran") -> dict:
    """
    Web search service in [Divar](https://divar.ir)
    """
    request = await client.request(method="GET", url=f"https://divar.ir/s/{city}?q={query}")
    if request.status_code != httpx.codes.OK:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "data": None,
            "error_message": "A problem has occurred on our end"
        }

    request = request.text
    start, finish = request.rfind("["), request.rfind("]")

    values = str()
    computed_value = list(request)[start:finish]
    for index in range(len(computed_value)):
        values += computed_value[index]

    values += "]"
    final_values = literal_eval(node_or_string=values)
    return {
        "success": True,
        "data": final_values,
        "error_message": None
    }
