import os
import asyncio
import discord
import shutil
import re
import random
import sys
import time
import requests

from utils.helpers import (
    clear_console,
    resource_path,
    get_env_path,
    load_instructions,
    load_config,
)
from utils.db import init_db, get_channels, get_ignored_users
from utils.error_notifications import webhook_log
from colorama import init, Fore, Style

init()


def check_config():
    env_path = resource_path("config/.env")
    config_path = resource_path("config/config.yaml")
    if not os.path.exists(env_path) or not os.path.exists(config_path):
        print("Config files are not setup! Running setup...")
        import utils.setup as setup

        setup.create_config()


def check_for_update():
    url = "https://api.github.com/repos/Najmul190/Discord-AI-Selfbot/releases/latest"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()["tag_name"]
    else:
        return None


current_version = "v2.0.0"
latest_version = check_for_update()
update_available = latest_version and latest_version != current_version

if update_available:
    print(
        f"{Fore.RED}A new version of the AI Selfbot is available! Please update to {latest_version} at: \nhttps://github.com/Najmul190/Discord-AI-Selfbot/releases/latest{Style.RESET_ALL}"
    )

    time.sleep(5)

check_config()
config = load_config()

from utils.ai import init_ai
from dotenv import load_dotenv
from discord.ext import commands
from utils.ai import generate_response, generate_response_image
from utils.split_response import split_response
from datetime import datetime
from collections import deque
from asyncio import Lock

env_path = get_env_path()

load_dotenv(dotenv_path=env_path, override=True)

init_db()
init_ai()

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = config["bot"]["prefix"]
OWNER_ID = config["bot"]["owner_id"]
TRIGGER = config["bot"]["trigger"].lower().split(",")
DISABLE_MENTIONS = config["bot"]["disable_mentions"]

bot = commands.Bot(command_prefix=PREFIX, help_command=None)

bot.owner_id = OWNER_ID
bot.active_channels = set(get_channels())
bot.ignore_users = get_ignored_users()
bot.message_history = {}
bot.paused = False
bot.allow_dm = config["bot"]["allow_dm"]
bot.allow_gc = config["bot"]["allow_gc"]
bot.help_command_enabled = config["bot"]["help_command_enabled"]
bot.realistic_typing = config["bot"]["realistic_typing"]
bot.anti_age_ban = config["bot"]["anti_age_ban"]
bot.batch_messages = config["bot"]["batch_messages"]
bot.batch_wait_time = float(config["bot"]["batch_wait_time"])
bot.user_message_counts = {}
bot.user_cooldowns = {}

bot.instructions = load_instructions()

bot.message_queues = {}
bot.processing_locks = {}
bot.user_message_batches = {}

bot.active_conversations = {}
CONVERSATION_TIMEOUT = 150.0

SPAM_MESSAGE_THRESHOLD = 5
SPAM_TIME_WINDOW = 10.0
COOLDOWN_DURATION = 60.0

MAX_HISTORY = 15


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

    if update_available:
        print(
            f"{Fore.RED}A new version of the AI Selfbot is available! Please update to {latest_version} at: \nhttps://github.com/Najmul190/Discord-AI-Selfbot/releases/latest{Style.RESET_ALL}\n"
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


@bot.event
async def setup_hook():
    await load_extensions()  # this loads the cogs on bot startup


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

    conv_key = f"{message.author.id}-{message.channel.id}"
    in_conversation = (
        conv_key in bot.active_conversations
        and time.time() - bot.active_conversations[conv_key] < CONVERSATION_TIMEOUT
    )

    content_has_trigger = any(
        re.search(rf"\b{re.escape(keyword)}\b", message.content.lower())
        for keyword in TRIGGER
    )

    if (
        content_has_trigger
        or mentioned
        or replied_to
        or is_dm
        or is_group_dm
        or in_conversation
    ):
        bot.active_conversations[conv_key] = time.time()

    return (
        content_has_trigger
        or mentioned
        or replied_to
        or is_dm
        or is_group_dm
        or in_conversation
    )


def update_message_history(author_id, message_content):
    if author_id not in bot.message_history:
        bot.message_history[author_id] = []
    bot.message_history[author_id].append(message_content)
    bot.message_history[author_id] = bot.message_history[author_id][-MAX_HISTORY:]


async def generate_response_and_reply(message, prompt, history, image_url=None):
    if not bot.realistic_typing:
        async with message.channel.typing():
            if image_url:
                response = await generate_response_image(
                    prompt, bot.instructions, image_url, history
                )
            else:
                response = await generate_response(prompt, bot.instructions, history)
    else:
        if image_url:
            response = await generate_response_image(
                prompt, bot.instructions, image_url, history
            )
        else:
            response = await generate_response(prompt, bot.instructions, history)

    chunks = split_response(response)

    if len(chunks) > 3:
        chunks = chunks[:3]
        print(f"{datetime.now().strftime('[%H:%M:%S]')} Response too long, truncating.")

    for chunk in chunks:
        if DISABLE_MENTIONS:
            chunk = chunk.replace(
                "@", "@\u200b"
            )  # prevent mentions by replacing them with a hidden whitespace

        if bot.anti_age_ban:
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
            if bot.realistic_typing:
                await asyncio.sleep(random.randint(10, 30))

                async with message.channel.typing():
                    characters_per_second = random.uniform(5.0, 6.0)
                    await asyncio.sleep(
                        int(len(chunk) / characters_per_second)
                    )  # around 50-70 wpm which is average typing speed

            try:
                if isinstance(message.channel, discord.DMChannel):
                    sent_message = await message.channel.send(chunk)
                else:
                    sent_message = await message.reply(
                        chunk,
                        mention_author=(True if config["bot"]["reply_ping"] else False),
                    )

                conv_key = f"{message.author.id}-{message.channel.id}"
                bot.active_conversations[conv_key] = time.time()

                if chunk == chunks[-1]:
                    channel_id = message.channel.id
                    batch_start_time = time.time()

                    while time.time() - batch_start_time <= bot.batch_wait_time:
                        try:

                            def check(m):
                                return (
                                    m.author.id == message.author.id
                                    and m.channel.id == message.channel.id
                                )

                            follow_up = await bot.wait_for(
                                "message",
                                timeout=bot.batch_wait_time
                                - (time.time() - batch_start_time),
                                check=check,
                            )

                            if channel_id not in bot.message_queues:
                                bot.message_queues[channel_id] = deque()
                                bot.processing_locks[channel_id] = Lock()

                            bot.message_queues[channel_id].append(follow_up)

                        except asyncio.TimeoutError:
                            break

                    if (
                        bot.message_queues[channel_id]
                        and not bot.processing_locks[channel_id].locked()
                    ):
                        asyncio.create_task(process_message_queue(channel_id))

            except discord.errors.HTTPException as e:
                print(
                    f"{datetime.now().strftime('[%H:%M:%S]')} Error replying to message, original message may have been deleted."
                )
                print_separator()

                await webhook_log(message, e)
            except discord.errors.Forbidden:
                print(
                    f"{datetime.now().strftime('[%H:%M:%S]')} Missing permissions to send message, bot may be muted."
                )
                print_separator()

                await webhook_log(message, e)
            except Exception as e:
                print(f"{datetime.now().strftime('[%H:%M:%S]')} Error: {e}")
                print_separator()

                await webhook_log(message, e)
        except discord.errors.Forbidden:
            print(
                f"{datetime.now().strftime('[%H:%M:%S]')} Missing permissions to send message, bot may be muted."
            )
            print_separator()

            await webhook_log(
                message, "Missing permissions to send message, bot may be muted."
            )

    return response


@bot.event
async def on_message(message):
    if should_ignore_message(message) and not message.author.id == bot.owner_id:
        return

    if message.content.startswith(PREFIX):
        await bot.process_commands(message)
        return

    channel_id = message.channel.id
    user_id = message.author.id
    current_time = time.time()

    batch_key = f"{user_id}-{channel_id}"
    is_followup = batch_key in bot.user_message_batches
    is_trigger = is_trigger_message(message)

    if (is_trigger or is_followup) and not bot.paused:
        if user_id in bot.user_cooldowns:
            cooldown_end = bot.user_cooldowns[user_id]
            if current_time < cooldown_end:
                remaining = int(cooldown_end - current_time)
                print(
                    f"{datetime.now().strftime('[%H:%M:%S]')} User {message.author.name} is on cooldown for {remaining}s"
                )
                return
            else:
                del bot.user_cooldowns[user_id]

        if user_id not in bot.user_message_counts:
            bot.user_message_counts[user_id] = []

        bot.user_message_counts[user_id] = [
            timestamp
            for timestamp in bot.user_message_counts[user_id]
            if current_time - timestamp < SPAM_TIME_WINDOW
        ]

        bot.user_message_counts[user_id].append(current_time)

        if len(bot.user_message_counts[user_id]) > SPAM_MESSAGE_THRESHOLD:
            bot.user_cooldowns[user_id] = current_time + COOLDOWN_DURATION
            print(
                f"{datetime.now().strftime('[%H:%M:%S]')} User {message.author.name} has been put on {COOLDOWN_DURATION}s cooldown for spam"
            )
            bot.user_message_counts[user_id] = []
            return

        if channel_id not in bot.message_queues:
            bot.message_queues[channel_id] = deque()
            bot.processing_locks[channel_id] = Lock()

        bot.message_queues[channel_id].append(message)

        if not bot.processing_locks[channel_id].locked():
            asyncio.create_task(process_message_queue(channel_id))


async def process_message_queue(channel_id):
    async with bot.processing_locks[channel_id]:
        while bot.message_queues[channel_id]:
            message = bot.message_queues[channel_id].popleft()
            batch_key = f"{message.author.id}-{channel_id}"
            current_time = time.time()

            if bot.batch_messages:
                if batch_key not in bot.user_message_batches:
                    first_image_url = (
                        message.attachments[0].url if message.attachments else None
                    )
                    bot.user_message_batches[batch_key] = {
                        "messages": [],
                        "last_time": current_time,
                        "image_url": first_image_url,
                    }
                    bot.user_message_batches[batch_key]["messages"].append(message)

                    await asyncio.sleep(bot.batch_wait_time)

                    while bot.message_queues[channel_id]:
                        if (
                            bot.message_queues[channel_id][0].author.id
                            == message.author.id
                        ):
                            next_message = bot.message_queues[channel_id].popleft()
                            if next_message.content not in [
                                m.content
                                for m in bot.user_message_batches[batch_key]["messages"]
                            ]:
                                bot.user_message_batches[batch_key]["messages"].append(
                                    next_message
                                )

                            if (
                                not bot.user_message_batches[batch_key]["image_url"]
                                and next_message.attachments
                            ):
                                bot.user_message_batches[batch_key]["image_url"] = (
                                    next_message.attachments[0].url
                                )
                        else:
                            break

                    messages_to_process = bot.user_message_batches[batch_key][
                        "messages"
                    ]
                    seen = set()
                    unique_messages = []
                    for msg in messages_to_process:
                        if msg.content not in seen:
                            seen.add(msg.content)
                            unique_messages.append(msg)

                    combined_content = "\n".join(msg.content for msg in unique_messages)
                    message_to_reply_to = unique_messages[-1]
                    image_url = bot.user_message_batches[batch_key]["image_url"]

                    del bot.user_message_batches[batch_key]
            else:
                combined_content = message.content
                message_to_reply_to = message
                image_url = message.attachments[0].url if message.attachments else None

            for mention in message_to_reply_to.mentions:
                combined_content = combined_content.replace(
                    f"<@{mention.id}>", f"@{mention.display_name}"
                )

            key = f"{message_to_reply_to.author.id}-{message_to_reply_to.channel.id}"
            if key not in bot.message_history:
                bot.message_history[key] = []

            bot.message_history[key].append(
                {"role": "user", "content": combined_content}
            )
            history = bot.message_history[key]

            if (
                message_to_reply_to.channel.id in bot.active_channels
                or (
                    isinstance(message_to_reply_to.channel, discord.GroupChannel)
                    and bot.allow_gc
                )
                or (
                    isinstance(message_to_reply_to.channel, discord.DMChannel)
                    and bot.allow_dm
                )
            ):
                response = await generate_response_and_reply(
                    message_to_reply_to, combined_content, history, image_url
                )
                bot.message_history[key].append(
                    {"role": "assistant", "content": response}
                )


async def load_extensions():
    if getattr(sys, "frozen", False):
        cogs_dir = os.path.join(sys._MEIPASS, "cogs")
    else:
        cogs_dir = os.path.join(os.path.abspath("."), "cogs")

    if not os.path.exists(cogs_dir):
        print(f"Warning: Cogs directory not found at {cogs_dir}. Skipping cog loading.")
        return

    clear_console()

    for filename in os.listdir(cogs_dir):
        if filename.endswith(".py"):
            cog_name = f"cogs.{filename[:-3]}"
            try:
                print(f"Loading cog: {cog_name}")
                await bot.load_extension(cog_name)
            except Exception as e:
                print(f"Error loading cog {cog_name}: {e}")


if __name__ == "__main__":
    bot.run(TOKEN, log_handler=None)
