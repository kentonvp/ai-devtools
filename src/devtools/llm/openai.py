from devtools.llm.client_interface import IClient
from devtools.config import SYSTEM_PROMPT
from openai import OpenAI
from rich import print


class OpenAIClient(IClient):
    def __init__(self, *, auth: dict, config: dict):
        """
        Initializes the object with provided authentication and configuration dictionaries.

        Args:
            auth (dict): The dictionary containing API key. It must contain an 'api_key' key.
            config (dict): The configuration dictionary. This can contain 'model' and
                           'system_prompt' keys. Defaults to 'gpt-4' for 'model' and
                           SYSTEM_PROMPT for 'system_prompt' if not provided.

        Raises:
            RuntimeError: If 'api_key' is not found in the 'auth' dictionary.
        """
        api_key = auth.get("api_key")
        if api_key is None:
            raise RuntimeError("Must set `api_key` in `auth` dictionary!!!")

        self.model = config.get("model", "gpt-4")
        self.system_prompt = config.get("system_prompt", SYSTEM_PROMPT)
        self.client = OpenAI(api_key=api_key)

    def send_prompt(self, prompt: str, **kwargs) -> str:
        """
        Sends a chat prompt to a client and receives a response.

        Args:
            prompt (str): The string to send as the user input.
            **kwargs: Additional key-value pairs to be passed to `completions.create`.

        Returns:
            str: The server's response to the chat prompt, or 'ERROR' if response content is None.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt,
                },
                {"role": "user", "content": prompt},
            ],
            temperature=1,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        if (res := response.choices[0].message.content) is not None:
            return res

        return "ERROR"
