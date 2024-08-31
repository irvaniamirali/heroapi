from duckduckgo_search import AsyncDDGS

output = {
    "success": True,
    "data": None,
    "error_message": None
}


async def text_query(query, region, safe_search, timelimit, backend, max_results):
    output["data"] = await AsyncDDGS().atext(query, region, safe_search, timelimit, backend, max_results)
    return output


async def news(query, max_results, region, safe_search, timelimit):
    output["data"] = await AsyncDDGS().anews(query, max_results, safe_search, region, timelimit)
    return output


async def chat(query, model, timeout):
    output["data"] = await AsyncDDGS().achat(query, model, timeout)
    return output


async def images(*args):
    output["data"] = await AsyncDDGS().aimages(*args)
    return output


async def videos(*args):
    output["data"] = await AsyncDDGS().avideos(*args)
    return output


async def answers(query):
    output["data"] = await AsyncDDGS().aanswers(query)
    return output


async def suggestions(query, region):
    output["data"] = await AsyncDDGS().asuggestions(query, region)
    return output


async def translate(text, from_lang, to_lang):
    output["data"] = await AsyncDDGS().atranslate(text, from_lang, to_lang)
    return output


async def maps(*args):
    output["data"] = await AsyncDDGS().amaps(*args)
    return output
