import os
import sys


def clear_console():
    """Clear the console screen."""
    os.system("cls" if os.name == "nt" else "clear")


def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_env_path():
    if getattr(sys, "frozen", False):
        return os.path.join(os.path.dirname(sys.executable), "config/.env")
    return os.path.join(os.path.abspath("."), "config/.env")
