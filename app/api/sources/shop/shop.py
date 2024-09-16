from ast import literal_eval

from user_agent import generate_user_agent

from httpx import AsyncClient

client = AsyncClient()

HEADERS = {
    "User_Agent": generate_user_agent()
}


async def divar(query, city):
    """
    Web search service in [Divar](https://divar.ir)
    """
    response = await client.request("GET", url=f"https://divar.ir/s/{city}?q={query}", headers=HEADERS)

    response = response.text
    start, finish = response.rfind("["), response.rfind("]")

    values = str()
    computed_value = list(response)[start:finish]
    for index in range(len(computed_value)):
        values += computed_value[index]

    values += "]"
    return literal_eval(node_or_string=values)
