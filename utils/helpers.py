import os
import sys
import yaml


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
    return resource_path("config/.env")


def load_config():
    config_path = resource_path("config/config.yaml")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        return config

    else:

        print(
            "Config file not found. Please provide a config file in config/config.yaml"
        )
        sys.exit(1)


def load_instructions():
    instructions_path = resource_path("config/instructions.txt")
    if os.path.exists(instructions_path):
        with open(instructions_path, "r", encoding="utf-8", errors="replace") as file:
            instructions = file.read()

        return instructions
    else:
        print("Instructions file not found. Using default instructions.")

        return ""
