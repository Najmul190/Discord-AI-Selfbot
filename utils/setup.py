import os
import yaml
import re
import sys
import requests

from time import sleep
from colorama import init, Fore, Style
from utils.helpers import resource_path, clear_console

init()


def validate_token(token):
    if not re.match(r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", token):
        return False

    headers = {"Authorization": token}
    try:
        r = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
        return r.status_code == 200
    except:
        return False


def validate_api_key(api_key, provider="openai"):
    if provider == "openai":
        if not api_key.startswith("sk-"):
            return False
        headers = {"Authorization": f"Bearer {api_key}"}
        try:
            r = requests.get("https://api.openai.com/v1/models", headers=headers)
            return r.status_code == 200
        except:
            return False
    elif provider == "groq":
        if not api_key.startswith("gsk_"):
            return False
        return True
    return False


def get_input(prompt, validator=None, default=None, password=False):
    while True:
        if default is not None and prompt == "Enter error webhook URL (optional - press enter to skip)":
            user_input = input(f"{prompt} (default: {default}): ").strip()
            if not user_input:
                return default
        else:
            if password:
                import getpass

                user_input = getpass.getpass(prompt + ": ").strip()
            else:
                user_input = input(prompt + ": ").strip()

        if not user_input and default is None:
            print(f"{Fore.RED}Input cannot be empty!{Style.RESET_ALL}")
            continue

        if validator:
            if validator(user_input):
                return user_input
            print(f"{Fore.RED}Invalid input! Please try again.{Style.RESET_ALL}")
            continue

        return user_input


def create_config():
    clear_console()

    print(f"\n{Fore.CYAN}=== AI Selfbot Setup Wizard ==={Style.RESET_ALL}\n")

    config = {
        "bot": {
            "owner_id": int(
                get_input(
                    "Enter your Discord user ID (can't be same as bot id)",
                    lambda x: x.isdigit(),
                )
            ),
            "prefix": get_input("Enter command prefix", default="~"),
            "trigger": get_input(
                "Enter trigger word(s) (comma-separated for multiple)"
            ),
            "groq_model": "llama3-70b-8192",
            "openai_model": "gpt-4o",
            "allow_dm": input("Allow DMs? (y/n): ").lower() == "y",
            "allow_gc": input("Allow group chats? (y/n): ").lower() == "y",
            "realistic_typing": input("Enable realistic typing? (y/n): ").lower()
            == "y",
            "batch_messages": True,
            "batch_wait_time": float(10),
            "anti_age_ban": True,
            "help_command_enabled": input(
                "Enable help command for everyone? (y/n): "
            ).lower()
            == "y",
            "disable_mentions": True,
            "reply_ping": True,
        },
        "notifications": {
            "error_webhook": get_input(
                "Enter error webhook URL (optional - press enter to skip)",
                lambda x: x.startswith("https://discord.com/api/webhooks/") or not x,
                default="",
            ),
            "ratelimit_notifications": input(
                "Enable webhook ratelimit notifications? (y/n): "
            ).lower()
            == "y",
        },
    }

    api_keys = {}
    provider = input("Choose AI provider (Groq/OpenAI): ").lower()
    if provider == "openai":
        api_keys["OPENAI_API_KEY"] = get_input(
            "Enter OpenAI API key (input will be hidden)",
            lambda x: validate_api_key(x, "openai"),
            password=True,
        )
    elif provider == "groq":
        api_keys["GROQ_API_KEY"] = get_input(
            "Enter Groq API key (input will be hidden)",
            lambda x: validate_api_key(x, "groq"),
            password=True,
        )

    token = get_input(
        "Enter Discord token (input will be hidden)", validate_token, password=True
    )
    api_keys["DISCORD_TOKEN"] = token

    config_dir = resource_path("config")
    os.makedirs(config_dir, exist_ok=True)

    with open(os.path.join(config_dir, ".env"), "w") as f:
        for key, value in api_keys.items():
            f.write(f"{key}={value}\n")

    with open(os.path.join(config_dir, "config.yaml"), "w") as f:
        yaml.safe_dump(config, f, default_flow_style=False)

    print(f"\n{Fore.GREEN}Setup complete! Configuration saved.{Style.RESET_ALL}")
    print(
        f"\n{Fore.LIGHTBLACK_EX}For help or support, join: https://discord.gg/yUWmzQBV4P{Style.RESET_ALL}"
    )

    sleep(3)


if __name__ == "__main__":
    create_config()
