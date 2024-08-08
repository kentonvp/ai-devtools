import argparse

from devtools import config
from devtools.docstringer import DocStringWriter
from devtools.lang_processor.python import PythonProcessor
from devtools.llm.openai_client import OpenAIClient

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Docstringify your code")
    parser.add_argument(
        "path", type=str, help="Path to the code you want to generate docstring for"
    )
    parser.add_argument(
        "--openai-api-key",
        type=str,
        help="OpenAI API Key",
        default=config.API_KEY,
        dest="openai_api_key",
    )
    args = parser.parse_args()

    client = OpenAIClient(auth={"api_key": args.openai_api_key}, config={})
    ds = DocStringWriter(client, PythonProcessor())

    ds.docstringify(args.path)
