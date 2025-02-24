import discord
import aiohttp

from datetime import datetime
from utils.helpers import load_config

config = load_config()


def print_error(error_type, error):
    print(f"{datetime.now().strftime('[%H:%M:%S]')} {error_type}: {error}")


async def webhook_log(ctx, error):
    webhook_url = config["notifications"]["error_webhook"]

    if webhook_url == "":
        return

    if ctx is None:
        if config["notifications"]["ratelimit_notifications"]:
            embed = discord.Embed(
                title="AI Selfbot Ratelimited",
                description=f"{error}",
                color=discord.Color.red(),
                timestamp=datetime.now(),
            )
        else:
            return
    elif isinstance(ctx, discord.Message):
        embed = discord.Embed(
            title="AI Selfbot Error",
            description=f"Message: `{ctx.content}`\nTrigger: {ctx.jump_url}\nError: `{error}`",
            color=discord.Color.red(),
            timestamp=datetime.now(),
        )
    elif isinstance(ctx, discord.ext.commands.Context):
        embed = discord.Embed(
            title="AI Selfbot Error",
            description=f"Command: `{ctx.command}`\nTrigger: {ctx.message.jump_url}\nError: `{error}`",
            color=discord.Color.red(),
            timestamp=datetime.now(),
        )
    else:
        embed = discord.Embed(
            title="AI Selfbot Error",
            description=f"Error: `{error}`",
            color=discord.Color.red(),
            timestamp=datetime.now(),
        )

    data = {
        "username": "AI Selfbot",
        "avatar_url": "https://cdn.discordapp.com/avatars/1040916971635621959/a_e52b4f8a9115021e5cc2e510232e8bd8.gif?size=256",
        "embeds": [embed.to_dict()],
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, json=data) as response:
                if response.status == 204:
                    pass
                else:
                    print_error("Webhook Error", f"Status: {response.status}")
    except Exception as e:
        print(f"Error while sending webhook: {e}")
