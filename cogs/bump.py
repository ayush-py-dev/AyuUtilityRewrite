import discord
from discord.ext import commands
import time
import aiosqlite

class Bump(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    """
    Check if the user has bumped the server using Disboard message
    """
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild is None: return
        if message.author.id == 302050872383242240 and "Bump done" in message.embeds[0].description: return