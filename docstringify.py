from devtools.docstringer import DocStringWriter
from devtools.lang_processor.python import PythonProcessor
from devtools.llm.openai import OpenAIClient
from devtools import config

if __name__ == "__main__":
    client = OpenAIClient(auth={"api_key": config.API_KEY}, config={})
    ds = DocStringWriter(client, PythonProcessor())

    ds.docstringify(".")
