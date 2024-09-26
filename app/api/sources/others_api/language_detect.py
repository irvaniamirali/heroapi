from fastapi import status

from langdetect import detect, LangDetectException


async def language_detect_api(response, text):
    """
    Identifying the language of texts
    """
    try:
        text_detected = detect(text)
        return {"language": text_detected}
    except LangDetectException:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "The value of the `text` parameter is not invalid."}
