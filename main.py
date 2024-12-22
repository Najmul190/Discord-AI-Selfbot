import os
import asyncio
import discord
import shutil
import re
import random

from dotenv import load_dotenv
from discord.ext import commands
from utils.ai import generate_response
from utils.split_response import split_response
from colorama import init, Fore, Style
from datetime import datetime

load_dotenv(dotenv_path="config/.env")
init()

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("PREFIX")
OWNER_ID = int(os.getenv("OWNER_ID", 0))
TRIGGER = os.getenv("TRIGGER", "").lower().split(",")

bot = commands.Bot(command_prefix=PREFIX, help_command=None)
bot.owner_id = OWNER_ID
bot.allow_dm = True
bot.allow_gc = True
bot.active_channels = set()
bot.ignore_users = []
bot.message_history = {}
bot.paused = False
bot.realistic_typing = os.getenv("REALISTIC_TYPING").lower()
bot.anti_age_ban = os.getenv("ANTI_AGE_BAN").lower()

MAX_HISTORY = 30


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


def get_terminal_size():
    columns, _ = shutil.get_terminal_size()
    return columns


def create_border(char="═"):
    width = get_terminal_size()
    return char * (width - 2)  # -2 for the corner characters


def print_header():
    width = get_terminal_size()
    border = create_border()
    title = "AI Selfbot by Najmul"
    padding = " " * ((width - len(title) - 2) // 2)

    print(f"{Fore.CYAN}╔{border}╗")
    print(f"║{padding}{Style.BRIGHT}{title}{Style.NORMAL}{padding}║")
    print(f"╚{border}╝{Style.RESET_ALL}")


def print_separator():
    print(f"{Fore.CYAN}{create_border('─')}{Style.RESET_ALL}")


@bot.event
async def on_ready():
    bot.selfbot_id = bot.user.id  # this has to be here, or else it won't work

    clear_console()

    print_header()
    print(
        f"AI Selfbot successfully logged in as {Fore.CYAN}{bot.user.name} ({bot.selfbot_id}){Style.RESET_ALL}.\n"
    )

    print("Active in the following channels:")

    for channel_id in bot.active_channels:
        channel = bot.get_channel(channel_id)
        if channel:
            try:
                print(f"- #{channel.name} in {channel.guild.name}")
            except Exception:
                pass

    print(
        f"\n{Fore.LIGHTBLACK_EX}Join the Discord server for support and news on updates: https://discord.gg/yUWmzQBV4P{Style.RESET_ALL}"
    )

    print_separator()


if os.path.exists("config/instructions.txt"):
    with open("config/instructions.txt", "r", encoding="utf-8") as file:
        instructions = file.read()
else:
    print(
        "Instructions file not found. Please provide instructions in config/instructions.txt"
    )
    exit(1)

if os.path.exists("config/channels.txt"):
    with open("config/channels.txt", "r") as f:
        for line in f:
            channel_id = int(line.strip())
            bot.active_channels.add(channel_id)
else:
    print("Active channels file not found. Creating a new one.")
    with open("config/channels.txt", "w"):
        pass

if os.path.exists("config/ignoredusers.txt"):
    with open("config/ignoredusers.txt", "r") as f:
        for line in f:
            user_id = int(line.strip())
            bot.ignore_users.append(user_id)
else:
    print("Ignored users file not found. Creating a new one.")
    with open("config/ignoredusers.txt", "w"):
        pass


def should_ignore_message(message):
    return (
        message.author.id in bot.ignore_users
        or message.author.id == bot.selfbot_id
        or message.author.bot
    )


def is_trigger_message(message):
    mentioned = (
        bot.user.mentioned_in(message)
        and "@everyone" not in message.content
        and "@here" not in message.content
    )
    replied_to = (
        message.reference
        and message.reference.resolved
        and message.reference.resolved.author.id == bot.selfbot_id
    )
    is_dm = isinstance(message.channel, discord.DMChannel) and bot.allow_dm
    is_group_dm = isinstance(message.channel, discord.GroupChannel) and bot.allow_gc

    content_has_trigger = any(
        re.search(rf"\b{re.escape(keyword)}\b", message.content.lower())
        for keyword in TRIGGER
    )

    return (
        content_has_trigger
        or mentioned
        or (replied_to and mentioned)
        or is_dm
        or is_group_dm
        and (mentioned or replied_to or content_has_trigger)
    )


def update_message_history(author_id, message_content):
    if author_id not in bot.message_history:
        bot.message_history[author_id] = []
    bot.message_history[author_id].append(message_content)
    bot.message_history[author_id] = bot.message_history[author_id][-MAX_HISTORY:]


async def generate_response_and_reply(message, prompt, history):
    response = await generate_response(prompt, instructions, history)
    chunks = split_response(response)

    if len(chunks) > 3:
        chunks = chunks[:3]
        print(f"{datetime.now().strftime('[%H:%M:%S]')} Response too long, truncating.")

    for chunk in chunks:
        chunk = chunk.replace(
            "@", "@\u200b"
        )  # Prevent mentions by replacing them with a hidden whitespace

        if bot.anti_age_ban == "true":
            chunk = re.sub(
                r"(?<!\d)([0-9]|1[0-2])(?!\d)|\b(zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\b",
                "\u200b",
                chunk,
                flags=re.IGNORECASE,
            )

        print(
            f'{datetime.now().strftime("[%H:%M:%S]")} {message.author.name}: {prompt}'
        )
        print(
            f'{datetime.now().strftime("[%H:%M:%S]")} Responding to {message.author.name}: {chunk}'
        )
        print_separator()

        try:
            if bot.realistic_typing == "true":
                await asyncio.sleep(random.randint(1, 5))

            async with message.channel.typing():
                if bot.realistic_typing == "true":
                    characters_per_second = random.uniform(5.0, 6.0)
                    await asyncio.sleep(
                        int(len(chunk) / characters_per_second)
                    )  # around 50-70 wpm which is average typing speed

                await message.reply(chunk)
        except Exception as e:
            print(f"Error sending message: {e}")

        await asyncio.sleep(1.5)

    return response


@bot.event
async def on_message(message):
    if should_ignore_message(message) and not message.author.id == bot.owner_id:
        return

    if message.content.startswith(PREFIX):
        await bot.process_commands(message)
        return

    if is_trigger_message(message) and not bot.paused:
        if message.reference and message.reference.resolved:
            if message.reference.resolved.author.id != bot.selfbot_id and (
                isinstance(message.channel, discord.DMChannel)
                or isinstance(message.channel, discord.GroupChannel)
            ):
                return

        for mention in message.mentions:
            message.content = message.content.replace(
                f"<@{mention.id}>", f"@{mention.display_name}"
            )

        author_id = str(message.author.id)
        update_message_history(author_id, message.content)

        if (
            message.channel.id in bot.active_channels
            or (isinstance(message.channel, discord.GroupChannel) and bot.allow_gc)
            or isinstance(message.channel, discord.DMChannel)
            and bot.allow_dm
        ):
            key = f"{message.author.id}-{message.channel.id}"
            if key not in bot.message_history:
                bot.message_history[key] = []
            bot.message_history[key].append(
                {"role": "user", "content": message.content}
            )
            history = bot.message_history[key]

            prompt = message.content

            response = await generate_response_and_reply(message, prompt, history)
            bot.message_history[key].append({"role": "assistant", "content": response})


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
            except Exception as e:
                print(f"Failed to load extension {filename}. Error: {e}")


if __name__ == "__main__":
    asyncio.run(load_extensions())
    asyncio.run(bot.run(token=TOKEN, log_handler=None))
