import os

API_KEY = os.getenv("OPENAI_API_KEY")

DOCSTRING_STYLE_TYPE = "Google Style"


def system_prompt(language: str) -> str:
    """
    Generates a system prompt for a technical writer.

    Args:
        language (str): The programming language in which the function is written.

    Returns:
        str: A message prompt detailing the requirements for writing a docstring.
    """
    return f"""You are an expert technical writer for a software company. You will be given the source code for a {language} function. If the function does NOT already provide a docstring, provide a {DOCSTRING_STYLE_TYPE} docstring that is grammatically correct and accurately describes the input function. The docstring should be terse and to the point only clarifying information that would be confusing to a mid level engineer. The docstring must be the only text in the response. Keep each line length to less than 80 characters. If there is already a docstring in the function the response should be empty."""
