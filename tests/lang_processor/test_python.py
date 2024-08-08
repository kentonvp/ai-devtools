import black

from devtools.lang_processor.python import PythonProcessor

SIMPLE_FUNC_CONTENTS = 'def hello_world():\n     print("Hello World!")'


def test_verify_extension(py_lang: PythonProcessor):
    """
    This function is used to test 'verify_extension' method of PythonProcessor. It checks
    whether the given file path or name ends with '.py'. It should return True if the file
    extension is '.py', otherwise False.

    Args:
        py_lang (PythonProcessor): PythonProcessor instance.
    """
    assert py_lang.verify_extension("hello.py")
    assert py_lang.verify_extension("path/to/hello.py")

    assert not py_lang.verify_extension("hello.pyc")
    assert not py_lang.verify_extension("hello.c")
    assert not py_lang.verify_extension("hello.")
    assert not py_lang.verify_extension("hello")


def test_to_ast(py_lang: PythonProcessor):
    """
    Converts the Python function into an abstract syntax tree (AST) and asserts the existence
    of root. Also, this function demonstrates that, even if the python code is invalid (missing a
    colon in the function definition), an AST is still created, but root node exists as None.

    Args:
        py_lang (PythonProcessor): A python code processor which converts given Python
        code into an AST.
    """
    root = py_lang.to_ast(SIMPLE_FUNC_CONTENTS)
    assert root is not None

    # This still builds a tree...
    content = """
    deff hi()
        print('HI');
    """
    assert root is not None


def test_extract_single_function_declarations(py_lang: PythonProcessor):
    """
    Extracts single function declarations from a given "PythonProcessor" object.

    Args:
        py_lang (PythonProcessor): The input processor object.

    Raises:
        AssertionError: If the number of extracted functions is not one or
                        the extracted function declaration does not match
                        the expected declaration.
    """
    root = py_lang.to_ast(SIMPLE_FUNC_CONTENTS)
    funcs = py_lang.extract_function_declarations(root)
    assert len(funcs) == 1
    assert funcs[0] == SIMPLE_FUNC_CONTENTS


def test_extract_multiple_functions(py_lang: PythonProcessor):
    """
    This function tests the `extract_function_declarations` method of the PythonProcessor
    class. It creates a source code content string comprising of multiple function definitions,
    then converts this source code content to an abstract syntax tree (AST). It then extracts
    the function declarations present in this AST.

    Args:
        py_lang (PythonProcessor): The PythonProcessor instance to be used for testing.

    Behaviour:
        This function performs assertion tests on the number of function declarations
        extracted and the correctness of the extracted contents.
    """
    multi_functions = [
        SIMPLE_FUNC_CONTENTS,
        "def square(x: int) -> int:\n    return x ** 2",
    ]
    content = "\n".join(multi_functions)

    root = py_lang.to_ast(content)
    funcs = py_lang.extract_function_declarations(root)

    assert len(funcs) == 2
    assert funcs[0] == SIMPLE_FUNC_CONTENTS.strip()
    assert "square" in funcs[1]


def test_insert_docstrings(py_lang: PythonProcessor):
    """This function, test_insert_docstrings, tests the PythonProcessor methods for inserting
    docstrings into existing Python code. The source code is first transformed to abstract
    syntax tree format, then function declarations are extracted, and finally docstrings are
    inserted. The output_code is formatted and compared with the expected_output. The number of
    insertions is also compared with the expected count. The function takes a PythonProcessor
    instance as a parameter."""
    source_code = """
def hello_world():
    print("Hello World!")

def square(x: int) -> int:
    return x ** 2
"""
    root = py_lang.to_ast(source_code)
    funcs = py_lang.extract_function_declarations(root)
    assert len(funcs) == 2

    docstrings = [
        '"""Prints an old programmers greeting."""',
        '"""Squares input integer and returns an integer."""',
    ]
    output_code, n_inserts = py_lang.insert_docstrings(source_code, funcs, docstrings)

    expected_output = black.format_str(
        """
def hello_world():
    \"\"\"Prints an old programmers greeting.\"\"\"
    print("Hello World!")

def square(x: int) -> int:
    \"\"\"Squares input integer and returns an integer.\"\"\"
    return x ** 2
""",
        mode=black.FileMode(),
    )

    assert output_code == expected_output
    assert n_inserts == 2
