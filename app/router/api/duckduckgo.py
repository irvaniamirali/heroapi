from duckduckgo_search import AsyncDDGS


async def text_query(query, region, safe_search, timelimit, backend, max_results):
    return await AsyncDDGS().atext(query, region, safe_search, timelimit, backend, max_results)


async def news(query, max_results, region, safe_search, timelimit):
    return await AsyncDDGS().anews(query, max_results, safe_search, region, timelimit)


async def chat(query, model, timeout):
    return await AsyncDDGS().achat(query, model, timeout)


async def images(*args):
    return await AsyncDDGS().aimages(*args)


async def videos(*args):
    return await AsyncDDGS().avideos(*args)


async def answers(query):
    return await AsyncDDGS().aanswers(query)


async def suggestions(query, region):
    return await AsyncDDGS().asuggestions(query, region)


async def translate(text, from_lang, to_lang):
    return await AsyncDDGS().atranslate(text, from_lang, to_lang)


async def maps(*args):
    return await AsyncDDGS().amaps(*args)
