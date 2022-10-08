from datetime import datetime
import discord
from discord.ext import commands
from config import *

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot=bot


    @commands.slash_command(guild_ids=[GUILD_ID],descripion="""Shows the Avatar""")
    async def _avatar(self,ctx,member:discord.Member=None):
        if not member:
            member=ctx.author
        em=discord.Embed(
            title=" ",
            description=f"Avatar of {member.mention}",
            color=discord.Color.dark_theme(),
            timestamp=datetime.utcnow()
        ).set_image(url=member.display_avatar)
        await ctx.respond(embed=em)
    
    @commands.user_command(guild_ids=[GUILD_ID],description="""Shows the avatar""")
    async def avatar(self,ctx,user:discord.Member):
        em=discord.Embed(
            title=" ",
            description=f"Avatar of {user.mention}",
            color=discord.Color.dark_theme(),
            timestamp=datetime.utcnow()
        ).set_image(
            url=user.display_avatar
        )
        await ctx.respond(embed=em)


def setup(bot):
    bot.add_cog(Avatar(bot))
    print("Cog loaded: Avatar")