import discord
from discord.ext import commands
from config import *
from datetime import datetime

class Suggeston(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def saccept(self,ctx,msgid:int, *, reason):
        """
        Accepts a suggestion
        **Syntax:** +saccept <message id> <reason>
        """
        chl=self.bot.get_channel(SUGGEST_CHL)
        msg: discord.Message = await chl.fetch_message(msgid)
        embed = discord.Embed(
            title="Suggestion Accepted",
            description=reason,
            color=discord.Color.green()
        )
        await msg.reply(embed=embed)
        await ctx.reply("Suggestion accepted!")
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sdeny(self,ctx,msgid:int, *, reason):
        """
        Denies a suggestion
        **Syntax:** +sdeny <message id> <reason>
        """
        chl=self.bot.get_channel(SUGGEST_CHL)
        msg: discord.Message = await chl.fetch_message(msgid)
        embed = discord.Embed(
            title="Suggestion Denied!",
            description=reason,
            color=discord.Color.red()
        )
        await msg.reply(embed=embed)
        await ctx.reply("Suggestion denied!")
        
    @commands.Cog.listener()
    async def on_message(self,msg:discord.Message):
        if msg.author.bot:
            return
        if msg.channel.id==SUGGEST_CHL:
            await msg.add_reaction("<:upvote:942683497204691014>")
            await msg.add_reaction("<:downvote:942683539541999666>")
            thread = await msg.create_thread(name=msg.content)
            await thread.send(
                embed=discord.Embed(
                    description="All the discussion will be here based on the suggestion:\n\n{msg.content}".format(msg=msg),
                    color=discord.Color.embed_background()
                )
            )

def setup(bot):
    bot.add_cog(Suggeston(bot))
    print("Cog loaded: Suggestion")