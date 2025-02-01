import os
import sys


def clear_console():
    """Clear the console screen."""
    os.system("cls" if os.name == "nt" else "clear")


def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        return os.path.join(os.path.dirname(sys.executable), relative_path)
    else:
        return os.path.join(os.path.abspath("."), relative_path)
