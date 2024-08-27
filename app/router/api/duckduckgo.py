from duckduckgo_search import AsyncDDGS

output = {
    "success": True,
    "data": None,
    "error_message": None
}


async def text_query(query, region, safe_search, timelimit, backend, max_results):
    result = await AsyncDDGS().atext(query, region, safe_search, timelimit, backend, max_results)
    output["data"] = result
    return output


async def news(query, max_results, region, safe_search, timelimit):
    query_result = await AsyncDDGS().anews(query, max_results, safe_search, region, timelimit)
    output["data"] = query_result
    return output


async def chat(query, model, timeout):
    query_result = await AsyncDDGS().achat(query, model, timeout)
    output["data"] = query_result
    return output


async def images(*args):
    query_result = await AsyncDDGS().aimages(*args)
    output["data"] = query_result
    return output


async def videos(*args):
    query_result = await AsyncDDGS().avideos(*args)
    output["data"] = query_result
    return output


async def answers(query):
    query_result = await AsyncDDGS().aanswers(query)
    output["data"] = query_result
    return output


async def suggestions(query, region):
    query_result = await AsyncDDGS().asuggestions(query, region)
    output["data"] = query_result
    return output


async def translate(text, from_lang, to_lang):
    query_result = await AsyncDDGS().atranslate(text, from_lang, to_lang)
    output["data"] = query_result
    return output


async def maps(*args):
    query_result = await AsyncDDGS().amaps(*args)
    output["data"] = query_result
    return output
