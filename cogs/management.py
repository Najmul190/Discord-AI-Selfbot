import discord
import os
import sys

from discord.ext import commands
from main import clear_console


class Management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
            await ctx.send(
                f"DMs are now {'allowed' if self.bot.allow_dm else 'disallowed'} for active channels."
            )

    @commands.command(name="togglegc", description="Toggle chatting in group chats.")
    async def togglegc(self, ctx):
        if ctx.author.id == self.bot.owner_id:
            self.bot.allow_gc = not self.bot.allow_gc
            await ctx.send(
                f"Group chats are now {'allowed' if self.bot.allow_gc else 'disallowed'} for active channels."
            )

    @commands.command()
    async def ignore(self, ctx, user: discord.User):
        try:
            if ctx.author.id == self.bot.owner_id:
                if user.id in self.bot.ignore_users:
                    self.bot.ignore_users.remove(user.id)
                    with open("config/ignoredusers.txt", "w") as f:
                        f.write("\n".join(map(str, self.bot.ignore_users)))
                    await ctx.send(f"Unignored {user.name}.")
                else:
                    self.bot.ignore_users.append(user.id)
                    with open("config/ignoredusers.txt", "a") as f:
                        f.write(str(user.id) + "\n")
                    await ctx.send(f"Ignoring {user.name}.")

        except Exception as e:
            await ctx.send(f"Error: {e}")

    @commands.command(name="toggleactive", description="Toggle active channels")
    async def toggleactive(self, ctx):
        if ctx.author.id == self.bot.owner_id:
            channel_id = ctx.channel.id
            if channel_id in self.bot.active_channels:
                self.bot.active_channels.remove(channel_id)
                with open("config/channels.txt", "w") as f:
                    for id in self.bot.active_channels:
                        f.write(str(id) + "\n")
                await ctx.send(
                    f"{'This DM' if isinstance(ctx.channel, discord.DMChannel) else 'This group' if isinstance(ctx.channel, discord.GroupChannel) else ctx.channel.mention} has been removed from the list of active channels."
                )
            else:
                self.bot.active_channels.add(channel_id)
                with open("config/channels.txt", "a") as f:
                    f.write(str(channel_id) + "\n")
                await ctx.send(
                    f"{'This DM' if isinstance(ctx.channel, discord.DMChannel) else 'This group' if isinstance(ctx.channel, discord.GroupChannel) else ctx.channel.mention} has been added to the list of active channels."
                )

    # @commands.command(
    #     name="setmodel",
    #     description="Set the model used for generating responses.",
    # )
    # For later :)

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
        description="Reloads all cogs.",
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

            await ctx.send("Reloaded all cogs.")

    @commands.command(
        name="restart",
        description="Restarts the bot.",
    )
    async def restart(self, ctx):
        if ctx.author.id == self.bot.owner_id:
            await ctx.send("Restarting bot...")
            clear_console()
            print("Restarting bot...")
            os.execv(sys.executable, ["python"] + sys.argv)


async def setup(bot):
    await bot.add_cog(Management(bot))
