import os
import asyncio
import discord
import shutil
import re

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
            print(f"- #{channel.name} in {channel.guild.name}")

    print_separator()

if os.path.exists("config/instructions.txt"):
    with open("config/instructions.txt", "r", encoding="utf-8") as file:
        instructions = file.read()

if os.path.exists("config/channels.txt"):
    with open("config/channels.txt", "r") as f:
        for line in f:
            channel_id = int(line.strip())
            bot.active_channels.add(channel_id)

if os.path.exists("config/ignoredusers.txt"):
    with open("config/ignoredusers.txt", "r") as f:
        for line in f:
            user_id = int(line.strip())
            bot.ignore_users.append(user_id)


def should_ignore_message(message):
    return (
        message.author.id in bot.ignore_users
        or message.author.id == bot.selfbot_id
        or message.author.bot
    )


def is_trigger_message(message):
    mentioned = bot.user.mentioned_in(message) and not (
        "@everyone" in message.content or "@here" in message.content
    )
    replied_to = (
        message.reference
        and message.reference.resolved
        and message.reference.resolved.author.id == bot.selfbot_id
    )
    is_dm = isinstance(message.channel, discord.DMChannel) and bot.allow_dm
    is_group_dm = isinstance(message.channel, discord.GroupChannel) and bot.allow_gc

    return (
        any(keyword in message.content.lower() for keyword in TRIGGER)
        or mentioned
        or (replied_to and mentioned)
        or is_dm
        or is_group_dm
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
        chunk = chunk.replace("@everyone", "@ everyone").replace("@here", "@ here")
        print(f'{datetime.now().strftime("[%H:%M:%S]")} {prompt}')
        print(
            f'{datetime.now().strftime("[%H:%M:%S]")} Responding to {message.author.name}: {chunk}'
        )
        print_separator()

        try:
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

    if is_trigger_message(message):
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

        #################### Put a # before each line ######################
        for t in TRIGGER:
            message.content = re.sub(
                rf"\b{t}\b", "ChatGPT", message.content, flags=re.IGNORECASE
            )
        ####################################################################

        author_id = str(message.author.id)
        update_message_history(author_id, message.content)

        if message.channel.id in bot.active_channels:
            key = f"{message.author.id}-{message.channel.id}"
            if key not in bot.message_history:
                bot.message_history[key] = []
            bot.message_history[key].append(
                {"role": "user", "content": message.content}
            )
            history = bot.message_history[key]
            prompt = f"{message.author.name}: {message.content}"

            async with message.channel.typing():
                response = await generate_response_and_reply(message, prompt, history)
                bot.message_history[key].append(
                    {"role": "assistant", "content": response}
                )


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
            except Exception as e:
                print(f"Failed to load extension {filename}. Error: {e}")


if __name__ == "__main__":
    asyncio.run(load_extensions())
    asyncio.run(bot.start(TOKEN))
