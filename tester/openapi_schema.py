import re
import random
import requests


def get_available_urls_from_openapi(root, openapi_json_path):
    req = requests.get(openapi_json_path)
    if req.status_code != 200:
        raise Exception("Could not get API Doc")

    content = req.json()
    paths = content["paths"]
    available_endpoints = []
    for path in paths.keys():
        if getattr(paths[path], "get") and path not in ["/docs", "/openapi.json"]:
            available_endpoints.append(f"{root}{path}")

    return available_endpoints


def set_custom_parameter_to_url(url, content_for_params):
    if "{" not in url or content_for_params is None:
        return url

    variadic_parameters = re.findall("{(.+?)}", url)
    substitution = {}
    for variadic_parameter in variadic_parameters:
        substitution[variadic_parameter] = content_for_params

    url = url.format(**substitution)
    return url


def set_test_urls(urls, contents):
    for url in urls:
        if len(contents) != 0 or "{" in url:
            random.shuffle(contents)
            for content in contents[:100]:
                yield set_custom_parameter_to_url(url, content)
        else:
            yield url
