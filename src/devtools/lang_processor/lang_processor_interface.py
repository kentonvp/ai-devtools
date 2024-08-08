from abc import ABC, abstractmethod

from tree_sitter import Language, Node, Parser


class ILanguageProcessor(ABC):
    @abstractmethod
    def __init__(self):
        """
        Initializes a new instance of the class.

        Args:
            ts_language (Language): An instance of `Language` class. Specifies the language
            in which the system operates.
        """
        pass

    @abstractmethod
    def verify_extension(self, file_path: str) -> bool:
        """
        Checks if the file at the provided path has an expected file extension.

        Args:
            file_path (str): The path to the file as a string.

        Returns:
            bool: Returns True if the file has the expected extension, False otherwise.
        """
        pass

    @abstractmethod
    def to_ast(self, content: str) -> Node:
        """
        Converts the given content into an Abstract Syntax Tree (AST) node object.

        Args:
            content (str): The text content which needs to be converted.

        Returns:
            Node: An AST node object representing the input content.
        """
        pass

    @abstractmethod
    def extract_function_declarations(self, root_node: Node) -> list[str]:
        """
        This function extracts function declarations from a given root node.

        Args:
            self: A reference to the current instance of the class.
            root_node (Node): The root node from which function declarations should be extracted.

        Returns:
            list[str]: A list of strings, each string being a function declaration.
        """
        pass

    @abstractmethod
    def insert_docstrings(
        self, source_code: str, functions: list[str], docstrings: list[str]
    ) -> tuple[str, int]:
        """
        Inserts docstrings into given Python source code.

        Args:
            source_code (str): The Python source code where the docstrings will be inserted.
            functions (list[str]): List of function names in the source code where the
                                   corresponding docstring needs to be inserted.
            docstrings (list[str]): List of docstrings that need to be inserted into
                                    the corresponding functions in the source code.

        Returns:
            tuple[str, int]: Tuple containing the modified source code with the inserted
                             docstring and the number of successful docstring insertions.
        """
        pass
