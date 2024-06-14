import os
import tempfile
from contextlib import contextmanager

from rich import print


@contextmanager
def mktemp(suffix: str):
    """
    This function generates a temporary file with a specified suffix, yields its path,
    and ultimately removes the file. It uses a context manager for safer file handling.

    Args:
        suffix (str): The suffix (extension) for the temporary file.

    Yields:
        (str): The path of the newly created temporary file.

    Raises:
        Exception: Any exception that occurs during file operation is printed to stdout.
        The executed file path is printed in case of exception.
    """
    file_path = tempfile.mktemp(suffix=suffix)
    try:
        yield file_path
    except Exception as e:
        print(e)
        print(f"file: {file_path}")
    finally:
        os.remove(file_path)
