from fastapi import APIRouter, Response, status

import codecs
import base64

from binascii import Error

router = APIRouter()


@router.get("/bs64encode", tags=["Base64"], status_code=status.HTTP_200_OK)
@router.post("/bs64encode", tags=["Base64"], status_code=status.HTTP_200_OK)
async def base64encode(text: str) -> dict:
    """
    Encode to Base64 format
    """
    string = codecs.encode(text, "utf-8")
    output = base64.b64encode(string)
    return {
        "success": True,
        "data": output,
        "error_message": None
    }


@router.get("/bs64decode", tags=["Base64"], status_code=status.HTTP_200_OK)
@router.post("/bs64decode", tags=["Base64"], status_code=status.HTTP_200_OK)
async def b64decode(response: Response, text: str) -> dict:
    """
    Decode from Base64 format
    """
    string = codecs.encode(text, "utf-8")
    try:
        output = base64.b64decode(string)
        return {
            "success": True,
            "data": output,
            "error_message": None
        }
    except Error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "data": None,
            "error_message": "This text not base64"
        }
