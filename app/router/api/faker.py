from json import loads
from random import choice

import aiofiles


async def name(count, language):
    filename = "data/name_fa.json"
    if language.startswith("en"):
        filename = "data/name_en.json"

    names = []
    async with aiofiles.open(filename, "r") as file:
        contents = await file.read()
        contents = loads(contents)
        for _ in range(count):
            names.append(choice(contents["items"]))
    return names


async def email(count):
    emails = []
    async with aiofiles.open("data/email_en.json", "r") as file:
        contents = await file.read()
        contents = loads(contents)
        for _ in range(count):
            emails.append(choice(contents["items"]))
    return emails


async def text(language):
    """
    Return text from json file
    """
    filename = "data/text_fa.json"
    if language.startswith("en"):
        filename = "data/text_en.json"

    async with aiofiles.open(filename, "r") as file:
        contents = await file.read()
        return loads(contents)
