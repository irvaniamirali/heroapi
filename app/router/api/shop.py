from ast import literal_eval

from httpx import AsyncClient

client = AsyncClient()


async def divar(query, city):
    """
    Web search service in [Divar](https://divar.ir)
    """
    request = await client.request("GET", url=f"https://divar.ir/s/{city}?q={query}")

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
