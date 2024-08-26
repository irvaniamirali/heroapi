from fastapi import status

import codecs
import base64

from binascii import Error


async def base64encode(text):
    """
    Encode to Base64 format
    """
    string = codecs.encode(text, "utf-8")
    return base64.b64encode(string)


async def b64decode(response, string, payload):
    """
    Decode from Base64 format
    """
    string = codecs.encode(string, "utf-8")
    try:
        output = base64.b64decode(string)
        payload["data"] = output
    except Error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        payload["success"] = False
        payload["error_message"] = "This text is not base64"
