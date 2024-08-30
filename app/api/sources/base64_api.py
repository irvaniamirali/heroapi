from fastapi import status

import codecs
import base64

from binascii import Error


async def base64encode(text):
    """
    Encode to Base64 format
    """
    string = codecs.encode(text, "utf-8")
    return {
        "success": True,
        "data": base64.b64encode(string),
        "error_message": None
    }


async def base64decode(response, string):
    """
    Decode from Base64 format
    """
    output = codecs.encode(string, "utf-8")
    try:
        return {
            "success": True,
            "data": base64.b64decode(output),
            "error_message": None
        }
    except Error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "data": None,
            "error_message": "This text is not base64"
        }
