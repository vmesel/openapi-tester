import logging
import requests

import concurrent.futures

from .openapi_schema import *

def send_request(url):
    logging.warning(f'Sending request to {url}')
    try:
        req = requests.get(url)
        logging.warning(
            f'Request response from: {url} was: {req.status_code} elapsed in {req.elapsed.total_seconds()}'
        )
    except requests.exceptions.SSLError:
        logging.error(f'Failed to send request to: {url}')


class Tester:
    def __init__(self,
            openapi_schema_url,
            api_url,
            slugs_file=None,
            max_threads = 4,
            concurrent_threads = 3
        ):
        if openapi_schema_url is None:
            raise Exception("Missing Schema URL")
        self.openapi_schema_url = openapi_schema_url

        if api_url is None:
            raise Exception("Missing API Root URL")
        self.api_url = api_url

        self.__urls_to_test = get_available_urls_from_openapi(
            self.api_url, self.openapi_schema_url
        )
        self.max_threads = max_threads
        self.concurrent_threads = concurrent_threads

        self.__slugs = []

        if slugs_file:
            with open(slugs_file, "r") as slugs_file_content:
                self.__slugs = slugs_file_content.readlines()

    def execute(self):
        logging.warning(f"Starting tests on: {self.api_url}!")
        urls = set_test_urls(
            self.__urls_to_test,
            self.__slugs
        )
        with concurrent.futures.ThreadPoolExecutor(self.max_threads) as executor:
            futures = [executor.submit(send_request, url) for url in urls]
            for future in futures:
                future.result()
        logging.info(f"URLs and Substitutions set and running!")


