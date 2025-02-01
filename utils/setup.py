import os
from utils.helpers import clear_console, resource_path


def prompt_env_values():
    clear_console()

    print("Configuring environment variables...")
    discord_token = input(
        "Enter the Discord Token of the account you'd like to run the AI on: "
    ).strip()

    while not discord_token:
        print("Discord Token cannot be empty!")
        discord_token = input(
            "Enter the Discord Token of the account you'd like to run the AI on: "
        ).strip()

    clear_console()

    groq_api_key = input(
        "Enter your Groq API Key (https://console.groq.com/keys) (Press Enter to skip if you're using ChatGPT): "
    ).strip()

    while groq_api_key and len(groq_api_key) < 10:
        print("Invalid Groq API Key!")
        groq_api_key = input(
            "Enter your Groq API Key (https://console.groq.com/keys) (Press Enter to skip if you're using ChatGPT): "
        ).strip()

    clear_console()

    openai_api_key = input(
        "Enter your OpenAI API Key (Optional - Press Enter to skip): "
    ).strip()

    while openai_api_key and len(openai_api_key) < 10:
        print("Invalid OpenAI API Key!")
        openai_api_key = input(
            "Enter your OpenAI API Key (Optional - Press Enter to skip): "
        ).strip()

    clear_console()

    owner_id = input(
        "Enter your Discord User ID (cannot be same as AI account ID): "
    ).strip()

    while not owner_id:
        print("Owner ID cannot be empty!")
        owner_id = input(
            "Enter your Discord User ID (cannot be same as AI account ID): "
        ).strip()

    clear_console()

    trigger = input(
        "Enter the trigger word for the AI (Add multiple by splitting them with commas - e.g: Trigger1,Trigger2,Trigger3): "
    ).strip()

    while not trigger:
        print("Trigger word cannot be empty!")
        trigger = input(
            "Enter the trigger word for the AI (Add multiple by splitting them with commas - e.g: Trigger1,Trigger2,Trigger3): "
        ).strip()

    clear_console()

    instructions = input(
        "Enter your custom instructions for the AI (Optional - Press Enter to use default): "
    ).strip()

    clear_console()

    if not openai_api_key:
        openai_api_key = ""

    env_path = resource_path("config/.env")
    os.makedirs(os.path.dirname(env_path), exist_ok=True)

    with open(env_path, "w") as env_file:
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
        env_file.write("ANTI_AGE_BAN=false\n")
        env_file.write(
            "\n\n# For any help or support, please join the support server: https://discord.gg/yUWmzQBV4P"
        )

    instructions_path = resource_path("config/instructions.txt")
    with open(instructions_path, "w") as instructions_file:
        if instructions:
            instructions_file.write(instructions)
        else:
            instructions_file.write(
                f"Act as a normal user on Discord and type in only lowercase, and NEVER reveal that you are in fact an AI. People will refer to you as {trigger}. They should be so human-like, nobody can even tell they're AI. Try incorporate emojis, common slang, but don't over do it by doing it every single message. As a normal discord user, you may use slang, emojis and other forms of communication that are common on Discord. Only speak in English, and pretend that you do not know any other languages. Make sure not to reveal you are AI. Don't keep adding asterisks in the first few words of your sentences, try and act like a normal human so try not to always offer assistance. Users may attempt to try and trick you into saying slurs, or things that can get you punished, so be cautious and if someone tells you to say something backwards, or repeat after them but with a certain condition refuse as it is most likely a trick to get you to break Discord TOS. Therefore, keep in mind the Discord TOS when you speak and ensure not to break any of the rules."
            )

    print(".env file created with your configurations in config/.env.")


def run_setup():
    try:
        prompt_env_values()
    except Exception as e:
        print(f"An error occurred during setup: {e}")
        print("Please try again or contact support.")


run_setup()
