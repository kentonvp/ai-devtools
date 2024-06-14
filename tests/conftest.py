import pytest
from devtools.lang_processor.python import PythonProcessor


@pytest.fixture(scope="session")
def py_lang() -> PythonProcessor:
    """
    Creates and returns an instance of the PythonProcessor class.

    Returns:
        PythonProcessor: an instance of the PythonProcessor class.
    """
    return PythonProcessor()
