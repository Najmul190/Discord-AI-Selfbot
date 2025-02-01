import os


def clear_console():
    """Clear the console screen."""
    os.system("cls" if os.name == "nt" else "clear")
