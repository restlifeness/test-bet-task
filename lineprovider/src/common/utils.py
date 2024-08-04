
import os


def is_pytest_running():
    """Return true if pytest is running"""
    return "PYTEST_CURRENT_TEST" in os.environ
