# Uses discord.py-self to run code on a Discord user account

import os
from opengpt.models.completion.chatbase.model import Model
import asyncio
import discord
import httpx
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
chatbase = Model()

prefix = "~"

owner_id = int(os.getenv("OWNER_ID"))
selfbot_id = int(os.getenv("SELFBOT_ID"))
trigger = os.getenv("TRIGGER")

bot = commands.Bot(command_prefix=prefix)
TOKEN = os.getenv("DISCORD_TOKEN")

allow_dm = True
active_channels = set()


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


async def generate_response(prompt):
    response = chatbase.GetAnswer(prompt=prompt, model="gpt-4")
    if not response:
        response = "I couldn't generate a response. Please try again."
    return response


def split_response(response, max_length=1900):
    words = response.split()
    chunks = []
    current_chunk = []

    for word in words:
        if len(" ".join(current_chunk)) + len(word) + 1 > max_length:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
        else:
            current_chunk.append(word)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


api_key = os.environ["HUGGING_FACE_API"]

API_URLS = [
    "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large",
    "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base",
    "https://api-inference.huggingface.co/models/nlpconnect/vit-gpt2-image-captioning",
    "https://api-inference.huggingface.co/models/ydshieh/vit-gpt2-coco-en",
]
headers = {"Authorization": f"Bearer {api_key}"}


async def fetch_response(client, api_url, data):
    response = await client.post(api_url, headers=headers, data=data, timeout=30)

    if response.status_code != 200:
        raise Exception(
            f"API request failed with status code {response.status_code}: {response.text}"
        )

    return response.json()


async def query(filename):
    with open(filename, "rb") as f:
        data = f.read()

    async with httpx.AsyncClient() as client:
        tasks = [fetch_response(client, api_url, data) for api_url in API_URLS]
        responses = []
        for task in asyncio.as_completed(tasks):
            try:
                response = await task
            except Exception as e:
                response = str(e)
            responses.append(response)

    return responses


async def download_image(image_url, save_as):
    async with httpx.AsyncClient() as client:
        response = await client.get(image_url)
    with open(save_as, "wb") as f:
        f.write(response.content)


async def process_image_link(image_url):
    temp_image = "temp_image.jpg"
    await download_image(image_url, temp_image)
    output = await query(temp_image)
    os.remove(temp_image)
    return output


instructions = """System : You are a large language model / LLM developed by OpenAI called Italiano. You will only speak English to the users unless specified otherwise. You are based on the GPT-3.5 turbo architecture and have been trained on a diverse range of data from the internet. You have the ability to see images by you're built in image to text model, but you will stil have to create captions for those images. Occasionally, the image to text may repeat in a pattern: 'a woman taking a self self self self self self self self self self self self self self self' would be 'A women taking a selfie.' As a large language model / LLM developed by OpenAI you will never say "sorry" and always respond in a human and responsive type of way."""
# To change the instructions, just replace everything between the three speech marks.

message_history = {}
MAX_HISTORY = 8


@bot.event
async def on_message(message):
    mentioned = bot.user.mentioned_in(message)
    replied_to = (
        message.reference
        and message.reference.resolved
        and message.reference.resolved.author.id == selfbot_id
    )

    if message.content.startswith("~"):
        await bot.process_commands(message)

    if message.author.id == selfbot_id:
        return

    if (
        any(keyword in message.content.lower() for keyword in [trigger.lower()])
        or mentioned
        or replied_to
    ):
        author_id = str(message.author.id)
        if author_id not in message_history:
            message_history[author_id] = []
        message_history[author_id].append(message.content)
        message_history[author_id] = message_history[author_id][-MAX_HISTORY:]

        if message.channel.id in active_channels:
            has_image = False
            image_caption = ""
            if message.attachments:
                for attachment in message.attachments:
                    if attachment.filename.lower().endswith(
                        (".png", ".jpg", ".jpeg", ".gif", ".bmp", "webp")
                    ):
                        caption = await process_image_link(attachment.url)
                        has_image = True
                        image_caption = f"\n[System : First note that some large image to text models will take time to load and may give out a timeout error but use the fallback models or the one that works.This how the caption is ranked 1st is main 2nd is secondary and 3rd is fallback model which  will gives worst caption one some cases. 1st and 2nd model sometimes takes a while to load so it can result in a error ignore that pls. Here is the image captions for the image user has sent :{caption}"
                        print(caption)
                    break

            if has_image:
                bot_prompt = f"{instructions}\n[System : Image context will be provided, generate an caption with a response for it. Don't mention about how image contexts are acquired, and don't mention about the chance hierachy."
            else:
                bot_prompt = f"{instructions}"
            user_prompt = "\n".join(message_history[author_id])
            prompt = f"{user_prompt}\n{bot_prompt}{message.author.name}: {message.content}\n{image_caption}\n{bot.user.name}:"
            async with message.channel.typing():
                response = await generate_response(prompt)
            print(response)
            chunks = split_response(response)
            for chunk in chunks:
                print(f"Responding to {message.author}: {chunk}")
                await message.reply(chunk)


@bot.command(name="ping", description="PONG")
async def ping(ctx):
    latency = bot.latency * 1000
    await ctx.send(f"Pong! Latency: {latency:.2f} ms")


@bot.command(name="toggledm", description="Toggle dm for chatting")
async def toggledm(ctx):
    if ctx.author.id == owner_id:
        global allow_dm
        allow_dm = not allow_dm
        await ctx.send(
            f"DMs are now {'allowed' if allow_dm else 'disallowed'} for active channels."
        )


@bot.command(name="toggleactive", description="Toggle active channels")
async def toggleactive(ctx):
    if ctx.author.id == owner_id:
        channel_id = ctx.channel.id
        if channel_id in active_channels:
            active_channels.remove(channel_id)
            with open("channels.txt", "w") as f:
                for id in active_channels:
                    f.write(str(id) + "\n")
            await ctx.send(
                f"{ctx.channel.mention} has been removed from the list of active channels."
            )
        else:
            active_channels.add(channel_id)
            with open("channels.txt", "a") as f:
                f.write(str(channel_id) + "\n")
            await ctx.send(
                f"{ctx.channel.mention} has been added to the list of active channels."
            )


# Read the active channels from channels.txt on startup
if os.path.exists("channels.txt"):
    with open("channels.txt", "r") as f:
        for line in f:
            channel_id = int(line.strip())
            active_channels.add(channel_id)


@bot.command(name="wipe", description="Clear bot's memory")
async def wipe(ctx):
    if ctx.author.id == owner_id:
        global message_history
        message_history.clear()
        await ctx.send("Wiped the bot's memory.")


bot.remove_command("help")


@bot.command(name="help", description="Get all other commands!")
async def help(ctx):
    help_text = """```
Bot Commands:
~pfp [image_url] - Change the bot's profile picture 
~wipe - Clears history of the bot
~ping - Shows the bot's latency
~toggleactive [channel] - Toggle the current channel to the list of active channels
~toggledm - Toggle if DM should be active or not

Created by Mishal#1916 + Najmul#0001```
    """

    await ctx.send(help_text)


bot.run(TOKEN)
