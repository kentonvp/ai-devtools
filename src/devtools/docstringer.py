import os
from devtools.llm.client_interface import IClient
from devtools.lang_processor.lang_processor_interface import ILanguageProcessor
from rich import print


class DocStringWriter:
    def __init__(self, client: IClient, parser: ILanguageProcessor) -> None:
        """
        This initializer method is for setting up the client and parser attributes.

        Args:
            client (ClientInterface): An instance of a class that implements the
                ClientInterface.
            parser (LanguageParserInterface): An instance of a class that implements
                the LanguageParserInterface.

        Returns:
            None
        """
        self.client = client
        self.parser = parser

    def generate_docstring(self, function_text: str) -> str:
        """
        This method generates a docstring for a given python function text.

        Args:
            function_text (str): The text of the python function.

        Returns:
            str: The docstring generated from the applied input function text.
        """
        prompt = f"```\n{function_text}\n```"
        return self.client.send_prompt(prompt)

    def docstringify(self, file_or_path: str, *, verbosity: int = 0) -> tuple[int, int]:
        """
        Traverses the directory or file given by 'file_or_path' and applies docstring insertion
        to all python files. If 'file_or_path' is a directory, recursively explores it to find
        all files.

        Args:
            file_or_path (str): A path to a directory or file.
            verbosity (int, optional): If set to a non-zero value, provides additional
                operation details. Default is 0.

        Returns:
            tuple[int, int]: A tuple where the first element is the number of directories
                traversed and the second element is the number of docstring insertions
                performed.
        """
        if os.path.isdir(file_or_path):
            n_dirs = 1
            n_insertions = 0
            for f in os.listdir(file_or_path):
                di, ni = self.docstringify(os.path.join(file_or_path, f))
                n_dirs += di
                n_insertions += ni
            return n_dirs, n_insertions

        elif os.path.isfile(file_or_path) and self.parser.verify_extension(
            file_or_path
        ):
            return 0, self.docstringify_file(file_or_path, verbosity=verbosity)

        return 0, 0

    def docstringify_file(self, file_path: str, *, verbosity: int = 0) -> int:
        """
        Generates and writes docstrings into a python source code file.

        Args:
            file_path (str): The path to the source code file.
            verbosity (int, optional): The verbosity level of the output. Defaults to 0.

        Returns:
            int: The number of docstrings inserted into the source code.
        """
        with open(file_path, "r") as f:
            source_code = f.read()
        # Parse the source code file
        root_node = self.parser.to_ast(source_code)

        # Extract function declarations
        functions = self.parser.extract_function_declarations(root_node)

        # Generate docstrings for each function
        docstrings = [self.generate_docstring(text) for text in functions]

        # Insert docstrings into the source code
        updated_code, n_insertions = self.parser.insert_docstrings(
            source_code, functions, docstrings
        )

        # Write the updated code back to the file
        if n_insertions > 0:
            with open(file_path, "w") as file:
                file.write(updated_code)

        if n_insertions > 1:
            print(f"Automagically generated {n_insertions} docstrings in {file_path}.")
        elif n_insertions == 1:
            print(f"Automagically generated {n_insertions} docstring in {file_path}.")
        elif verbosity > 0:
            print(f"No docstrings generated in {file_path}.")

        return n_insertions
