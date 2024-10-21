from fastapi import status

from codecs import encode
from base64 import b64decode as decode

from binascii import Error


async def b64encode(text):
    """
    Encode to Base64 format
    """
    string = encode(text, "utf-8")
    return {"output": decode(string)}


async def b64decode(response, string):
    """
    Decode from Base64 format
    """
    output = encode(string, "utf-8")
    try:
        return {"output": decode(output)}
    except Error:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "This text is not base64."}
