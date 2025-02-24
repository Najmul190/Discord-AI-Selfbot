import discord
import os
import sys
import subprocess
import yaml
import re
import asyncio

from discord.ext import commands
from utils.helpers import load_instructions, load_config, resource_path
from utils.db import (
    add_ignored_user,
    remove_ignored_user,
    remove_channel,
    add_channel,
)


class Management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def save_config(self, new_config):
        config_path = resource_path("config/config.yaml")

        with open(config_path, "w", encoding="utf-8") as file:
            yaml.dump(new_config, file, default_flow_style=False, allow_unicode=True)

    @commands.command(
        name="pause", description="Pause the bot from producing AI responses."
    )
    async def pause(self, ctx):
        if ctx.author.id == self.bot.owner_id:
            self.bot.paused = not self.bot.paused
            await ctx.send(
                f"{'Paused' if self.bot.paused else 'Unpaused'} the bot from producing AI responses."
            )

    @commands.command(name="toggledm", description="Toggle DM for chatting")
    async def toggledm(self, ctx):
        if ctx.author.id == self.bot.owner_id:
            self.bot.allow_dm = not self.bot.allow_dm

            config = load_config()

            config["bot"]["allow_dm"] = self.bot.allow_dm

            self.save_config(config)

            await ctx.send(
                f"DMs are now {'allowed' if self.bot.allow_dm else 'disallowed'} for active channels."
            )

    @commands.command(name="togglegc", description="Toggle chatting in group chats.")
    async def togglegc(self, ctx):
        if ctx.author.id == self.bot.owner_id:
            self.bot.allow_gc = not self.bot.allow_gc

            config = load_config()

            config["bot"]["allow_gc"] = self.bot.allow_gc

            self.save_config(config)

            await ctx.send(
                f"Group chats are now {'allowed' if self.bot.allow_gc else 'disallowed'} for active channels."
            )

    @commands.command()
    async def ignore(self, ctx, user: discord.User):
        try:
            if ctx.author.id == self.bot.owner_id:
                if user.id in self.bot.ignore_users:
                    self.bot.ignore_users.remove(user.id)

                    remove_ignored_user(user.id)

                    await ctx.send(f"Unignored {user.name}.")
                else:
                    self.bot.ignore_users.append(user.id)

                    add_ignored_user(user.id)

                    await ctx.send(f"Ignoring {user.name}.")

        except Exception as e:
            await ctx.send(f"Error: {e}")

    @commands.command(name="toggleactive", description="Toggle active channels")
    async def toggleactive(self, ctx, channel=None):
        if ctx.author.id == self.bot.owner_id:
            if channel is None:
                channel = ctx.channel
                channel_id = channel.id
            else:
                mention_match = re.match(r"<#(\d+)>", channel)
                if mention_match:
                    channel_id = int(mention_match.group(1))
                else:
                    channel_id = int(channel)

                try:
                    channel = await self.bot.fetch_channel(channel_id)
                except discord.errors.NotFound:
                    await ctx.send("Channel not found.")
                    return

            if channel_id in self.bot.active_channels:
                self.bot.active_channels.remove(channel_id)
                remove_channel(channel_id)
                await ctx.send(
                    f"{'This DM' if isinstance(ctx.channel, discord.DMChannel) else 'This group' if isinstance(ctx.channel, discord.GroupChannel) else channel.mention} has been removed from the list of active channels."
                )
            else:
                self.bot.active_channels.add(channel_id)
                add_channel(channel_id)
                await ctx.send(
                    f"{'This DM' if isinstance(ctx.channel, discord.DMChannel) else 'This group' if isinstance(ctx.channel, discord.GroupChannel) else channel.mention} has been added to the list of active channels."
                )

    @commands.command(
        name="wipe",
        description="Clears the bots message history, resetting it's memory.",
    )
    async def wipe(self, ctx):
        if ctx.author.id == self.bot.owner_id:
            self.bot.message_history.clear()
            await ctx.send("Wiped the bot's memory.")

    @commands.command(
        name="reload",
        description="Reloads all cogs and the bot instructions.",
    )
    async def reload(self, ctx):
        if ctx.author.id == self.bot.owner_id:
            for filename in os.listdir("./cogs"):
                if filename.endswith(".py"):
                    try:
                        await self.bot.unload_extension(f"cogs.{filename[:-3]}")
                        await self.bot.load_extension(f"cogs.{filename[:-3]}")

                    except Exception as e:
                        print(f"Failed to reload extension {filename}. Error: {e}")

                        await ctx.send(
                            f"Failed to reload {filename}. Check logs for details."
                        )

            self.bot.instructions = load_instructions()

            await ctx.send("Reloaded all cogs.")

    @commands.command(
        name="restart",
        description="Restarts the bot.",
    )
    async def restart(self, ctx):
        if ctx.author.id == self.bot.owner_id:
            await ctx.message.add_reaction("✅")

            print("Restarting bot...")

            if getattr(sys, "frozen", False):
                exe_path = sys.executable

                os.startfile(exe_path)

                await asyncio.sleep(3)

                await ctx.bot.close()
                sys.exit(0)
            else:
                python = sys.executable
                subprocess.Popen([python] + sys.argv)

                await ctx.bot.close()
                sys.exit(0)

    @commands.command(
        name="shutdown",
        description="Shuts down the bot.",
    )
    async def shutdown(self, ctx):
        if ctx.author.id == self.bot.owner_id:
            await ctx.message.add_reaction("✅")

            print("Shutting down bot...")

            await ctx.bot.close()
            sys.exit(0)

    @commands.command(
        name="instructions",
        description="View or change the AI prompt.",
        aliases=["prompt", "setprompt", "sp"],
    )
    async def instructions(self, ctx, *, prompt=None):
        if ctx.author.id == self.bot.owner_id:
            if prompt is None:
                await ctx.send(
                    f"Current prompt:\n{f'```{self.bot.instructions}```' if self.bot.instructions != '' else 'No prompt is currently set.'}"
                )
            elif prompt.lower() == "clear":
                self.bot.instructions = ""

                with open(resource_path("config/instructions.txt"), "w") as file:
                    file.write("")

                await ctx.send("Cleared prompt.")
            else:
                self.bot.instructions = prompt

                with open(resource_path("config/instructions.txt"), "w") as file:
                    file.write(prompt)

                await ctx.send(f"Updated prompt to:\n```{prompt}```")


async def setup(bot):
    await bot.add_cog(Management(bot))
