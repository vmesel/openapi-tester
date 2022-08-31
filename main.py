import argparse

import tester

parser = argparse.ArgumentParser(
    description="OpenAPI Tester is a tool for stress testing APIs.", prefix_chars="--"
)
parser.add_argument(
    "--api",
    type=str,
    metavar="api_url",
    help="the link for the api root - this URL must not end with /",
    required=True,
)

parser.add_argument(
    "--openapi_json_path",
    type=str,
    metavar="openapi_json_path",
    help="the link for the openapi.json file",
    required=True,
)

parser.add_argument(
    "--slugs_path",
    type=str,
    metavar="slugs_path",
    help="the link for the json with slugs file",
    required=False,
)

parser.add_argument(
    "--max_threads",
    type=str,
    metavar="max_threads",
    help="max threads for processing the requests",
    required=False,
)

parser.add_argument(
    "--concurrent_threads",
    type=str,
    metavar="concurrent_threads",
    help="number of concurrent threads",
    required=False,
)


if __name__ == "__main__":
    args = parser.parse_args()
    kwargs = {
        "openapi_schema_url": args.openapi_json_path,
        "api_url": args.api,
        "slugs_file": args.slugs_path,
    }
    if args.max_threads:
        kwargs["max_threads"] = args.max_threads
    
    if args.concurrent_threads:
        kwargs["concurrent_threads"] = args.concurrent_threads

    test = tester.Tester(
        **kwargs
    )
    test.execute()
