from discord.ext import commands
import discord
from config import *


class PinnedMsg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, react: discord.Reaction, user: discord.Member):
        if react.message.guild.id == GUILD_ID:
            msg = react.message
            if user.guild_permissions.manage_messages:
                if str(react.emoji) != "📌":
                    return
                await msg.pin(reason=f"Pinned by {user.name}#{user.discriminator}")
                em = discord.Embed(
                    title="",
                    description="📌 Pinned a message",
                    color=discord.Color.dark_teal()
                ).add_field(
                    name="Pin request by:",
                    value=user.mention
                ).add_field(
                    name="Jump URL",
                    value=f"[click here]({react.message.jump_url})"
                )
                logc = self.bot.get_channel(LOGS)
                await logc.send(embed=em)

    @commands.Cog.listener()
    async def on_reaction_remove(self, react: discord.Reaction, user: discord.Member):
        if react.message.guild.id == GUILD_ID:
            msg = react.message
            if user.guild_permissions.manage_messages:
                if str(react.emoji) != "📌":
                    return
                await msg.unpin(reason=f"Pinned Removed by {user.name}#{user.discriminator}")
                em = discord.Embed(
                    title="",
                    description="📌 Unpinned a message",
                    color=discord.Color.dark_teal()
                ).add_field(
                    name="Unpin request by:",
                    value=user.mention
                ).add_field(
                    name="Jump URL",
                    value=f"[click here]({react.message.jump_url})"
                )
                logc = self.bot.get_channel(LOGS)
                await logc.send(embed=em)


def setup(bot):
    bot.add_cog(PinnedMsg(bot))
    print("Cog loaded: PinnedMsg")
