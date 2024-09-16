from bs4 import BeautifulSoup


async def record_element_value(element, json_output):
    """
    Record the html element's value in the json_output.
    """
    element = element.strip()
    if element != "\n" and element != "":
        if json_output.get("_value"):
            json_output["_values"] = [json_output["_value"]]
            json_output["_values"].append(element)
            del json_output["_value"]
        elif json_output.get("_values"):
            json_output["_values"].append(element)
        else:
            json_output["_value"] = element


async def iterate(html_section, json_output, count, capture_element_values, capture_element_attributes):
    for part in html_section:
        if not isinstance(part, str):
            string_is_unicode = False
            if not string_is_unicode:
                if not json_output.get(part.name):
                    json_output[part.name] = []
                new_json_output_for_sub_parts = {}
                if part.attrs and capture_element_attributes:
                    new_json_output_for_sub_parts = {"_attributes": part.attrs}

                count += 1
                json_output[part.name].append(
                    await iterate(
                        part,
                        new_json_output_for_sub_parts,
                        count,
                        capture_element_values,
                        capture_element_attributes,
                    )
                )
        else:
            if capture_element_values:
                await record_element_value(part, json_output)
    return json_output


async def convert(html_string, capture_element_values=True, capture_element_attributes=True):
    """
    Convert HTML document to json
    """
    soup = BeautifulSoup(html_string, "html.parser")
    contents = [child for child in soup.contents]
    return await iterate(contents, {}, 0, capture_element_values, capture_element_attributes)


async def convert_html_to_json_api(html, capture_element_values, capture_element_attributes):
    """
    Convert HTML document to json
    """
    return await convert(html, capture_element_values, capture_element_attributes)
