import tree_sitter_python as tspython
from devtools.lang_processor.lang_processor_interface import ILanguageProcessor
from tree_sitter import Language, Node, Parser
import black


class PythonProcessor(ILanguageProcessor):
    def __init__(self):
        """
        Initializes the instance with the given tree-sitter language.

        Args:
            ts_language (Language): Tree-sitter language module.

        Attributes:
            parser (Parser): A Tree-sitter parser.
            language (Language): A Tree-sitter language module.
        """
        self.language = Language(tspython.language())
        self.parser = Parser()
        self.parser.language = self.language

    def verify_extension(self, file_path: str) -> bool:
        """
        Checks if a given file path ends with '.py' extension or not.

        Args:
            file_path (str): The path of the file to verify.

        Returns:
            bool: True if the file_path ends with '.py', False otherwise.
        """
        return file_path.endswith(".py")

    def to_ast(self, content: str) -> Node:
        """
        Converts the given string content into an Abstract Syntax Tree (AST).

        Args:
            content (str): The string to be converted.

        Returns:
            Node: The root node of the parsed AST.
        """
        tree = self.parser.parse(bytes(content, "utf8"))
        return tree.root_node

    def extract_function_declarations(self, root_node: Node) -> list[str]:
        """
        Extracts function declarations from the root node of a parse tree.

        Args:
            root_node (Node): The root node of a parse tree.

        Returns:
            list[str]: A list of strings where each string is a serialized representation
                       of a unique function declaration in the parse tree.
        """
        query = self.language.query(
            "(function_definition name: (identifier) @function_name)"
        )

        functions = []
        for match in query.captures(root_node):
            function_node = match[0].parent
            function_text = function_node.text.decode("utf8")
            functions.append(function_text)

        return functions

    def insert_docstrings(
        self, source_code: str, functions: list[str], docstrings: list[str]
    ) -> tuple[str, int]:
        """
        This function inserts docstrings into source_code at the beginning of each function specified
        in the `functions` list, corresponding to the `docstrings` list.

        Args:
            source_code (str): The python source code as a string.
            functions (list[str]): A list of functions' text from the source code.
            docstrings (list[str]): A list of docstrings to be inserted. An empty string means the
                                    corresponding function already contains a docstring.
        Returns:
            tuple: A tuple containing the formatted source code with inserted docstrings and the number
                   of inserted docstrings.

        Raises:
            AssertionError: If the number of functions does not equal to the number of docstrings.
            ValueError: If unable to identify the proper location for inserting the docstring.
        """
        assert len(functions) == len(
            docstrings
        ), f"`len(functions)={len(functions)}` != `len(docstrings)={len(docstrings)}`"
        updated_code = source_code
        insertions = 0
        for function_text, docstring in zip(functions, docstrings):
            # If the docstring is empty it means the function already contains a docstring.
            if not len(docstring.strip()):
                continue

            # Split the function text into lines
            lines = function_text.split("\n")

            # Find the index of the first line after the function header
            i = -1
            for i, line in enumerate(lines):
                if line.strip().endswith(":"):
                    break

            if i < 0:
                raise ValueError("Unable to find location for docstring")

            indent = " " * (len(lines[i + 1]) - len(lines[i + 1].lstrip()))

            # Insert the docstring after the function header
            lines.insert(i + 1, f"{indent}{docstring}")

            # Join the lines back into the updated function text
            updated_function_text = "\n".join(lines)

            # Replace the original function text with the updated one
            updated_code = updated_code.replace(function_text, updated_function_text)
            insertions += 1

        # Format the updated code using Black
        formatted_code = black.format_str(updated_code, mode=black.FileMode())
        return formatted_code, insertions
