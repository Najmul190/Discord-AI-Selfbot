import os


def clear_console():
    """Clear the console screen."""
    os.system("cls" if os.name == "nt" else "clear")


def prompt_env_values():
    """Prompt user for .env configuration values."""
    clear_console()
    print("Configuring environment variables...")
    discord_token = input(
        "Enter the Discord Token of the account you'd like to run the AI on: "
    ).strip()
    groq_api_key = input(
        "Enter your Groq API Key (https://console.groq.com/keys): "
    ).strip()
    openai_api_key = input(
        "Enter your OpenAI API Key (Optional - Press Enter to skip): "
    ).strip()
    owner_id = input(
        "Enter your Discord User ID (cannot be same as AI account ID): "
    ).strip()
    trigger = input(
        "Enter the trigger word for the AI (You can add numerous by splitting them with commas - e.g: Trigger1,Trigger2,Trigger3): "
    ).strip()

    if not openai_api_key:
        openai_api_key = ""

    # Write the configuration values to the .env file
    with open("config/.env", "w") as env_file:
        env_file.write("# # Token of the selfbot\n")
        env_file.write(f"DISCORD_TOKEN={discord_token}\n")

        env_file.write(
            "\n# Your API Key for GROQ API (https://console.groq.com/keys)\n"
        )
        env_file.write(f"GROQ_API_KEY={groq_api_key}\n")

        env_file.write(
            "\n# Your API Key for OpenAI (https://platform.openai.com/api_keys) (Optional - Leave blank to use free API)\n"
        )
        env_file.write(f"OPENAI_API_KEY={openai_api_key}\n")

        env_file.write("\n# Owner ID of your account (can't be same as bot's ID)\n")
        env_file.write(f"OWNER_ID={owner_id}\n")

        env_file.write("\n# The prefix for the bot\n")
        env_file.write("PREFIX=~\n")

        env_file.write(
            "\n# The word you want the AI to respond to (e.g: TRIGGER=John)\n"
        )
        env_file.write(f"TRIGGER={trigger}\n")

        env_file.write(
            "\n# Realistic Typing - If set to true, the bot will type for a realistic(ish) amount of time before sending a message\n"
        )
        env_file.write("REALISTIC_TYPING=false\n")

        env_file.write(
            "\n# Anti Age Ban Measures - The bot will attempt to avoid being banned by Discord by filtering out numbers below 13\n# This is a strict method, as it removes ANY number below 13, including dates, times, etc.\n"
        )
        env_file.write("ANTI_AGE_BAN=true\n")
        env_file.write(
            "\n\n# For any help or support, please join the support server: https://discord.gg/yUWmzQBV4P"
        )

    print(".env file created with your configurations in config/.env.")


def main():
    """Main script execution."""

    # Prompt user for .env configuration if .env file does not exist
    if not os.path.exists("config/.env"):
        prompt_env_values()
    else:
        print(".env file already exists. Skipping creation.")


if __name__ == "__main__":
    main()
