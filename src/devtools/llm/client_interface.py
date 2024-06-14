from abc import ABC


class IClient(ABC):
    def __init__(self, *, auth: dict):
        """
        Initializes the class instance but is not implemented.

        Raises:
            NotImplemented: This function is not designed to be called.

        Args:
            auth (dict): Dictionary containing authentication details. It is a keyword-only
                         argument.

        """
        raise NotImplemented()

    def send_prompt(self, prompt: str, **kwargs) -> str:
        """
        Sends a prompt message.
        This is an abstract function that should be implemented in subclasses.

        Args:
            prompt (str): The prompt message to be sent.

        Raises:
            NotImplemented: An error happens if the function is not implemented in
            a subclass.

        Returns:
            str: String with the response to the prompt.

        Note:
            Any additional keyword arguments (**kwargs) are ignored.
        """
        raise NotImplemented()
