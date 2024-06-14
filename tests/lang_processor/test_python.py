import black
from devtools.lang_processor.python import PythonProcessor
import pytest
from rich import print, print_json

SIMPLE_FUNC_CONTENTS = 'def hello_world():\n     print("Hello World!")'


def test_verify_extension(py_lang: PythonProcessor):
    assert py_lang.verify_extension("hello.py")
    assert py_lang.verify_extension("path/to/hello.py")

    assert not py_lang.verify_extension("hello.pyc")
    assert not py_lang.verify_extension("hello.c")
    assert not py_lang.verify_extension("hello.")
    assert not py_lang.verify_extension("hello")


def test_to_ast(py_lang: PythonProcessor):
    root = py_lang.to_ast(SIMPLE_FUNC_CONTENTS)
    assert root is not None

    # This still builds a tree...
    content = """
    deff hi()
        print('HI');
    """
    assert root is not None


def test_extract_single_function_declarations(py_lang: PythonProcessor):
    root = py_lang.to_ast(SIMPLE_FUNC_CONTENTS)
    funcs = py_lang.extract_function_declarations(root)
    assert len(funcs) == 1
    assert funcs[0] == SIMPLE_FUNC_CONTENTS


def test_extract_multiple_functions(py_lang: PythonProcessor):
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
