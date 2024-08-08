from devtools import config
from devtools.llm.openai_client import OpenAIClient


def create_openai_agent():
    """
    Creates and returns an instance of the OpenAIClient class.

    The OpenAIClient constructor takes in two arguments: an auth dictionary containing
    an 'api_key', and a config dictionary which is currently empty.

    Returns:
        OpenAIClient: An instance of OpenAIClient with the given API key as its
        authorization parameter.
    """
    return OpenAIClient(auth={"api_key": config.API_KEY}, config={})


AGENT_LIBRARY = {"openai": create_openai_agent}


def agent_factory(ai: str):
    """
    Creates an agent based on the provided AI identifier.

    Args:
        ai (str): The identifier of the AI agent to be created. This string should match an
        entry in AGENT_LIBRARY.

    Raises:
        KeyError: If the provided AI identifier does not exist in AGENT_LIBRARY.
    """
    if ai.lower() in AGENT_LIBRARY:
        AGENT_LIBRARY[ai.lower()]
