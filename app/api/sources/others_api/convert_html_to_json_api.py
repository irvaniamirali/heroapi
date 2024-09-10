import html_to_json


async def convert_html_to_json_api(html):
    """
    Convert HTML document to json
    """
    output_json = html_to_json.convert(html)
    return {
        "success": True,
        "data": output_json,
        "error_message": None
    }
