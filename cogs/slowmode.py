import discord
from discord.ext import commands, tasks

from config import GENERAL

msgss=0
slom=False

class Slowmode(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        await auto_slowmode.start(self.bot)

    @commands.command(aliases=["sm"])
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self,ctx,time:int=0):
        """
        Sets slowmode for the channel
        **Syntax:** +[slowmode|sm] [seconds]
        """
        await ctx.channel.edit(slowmode_delay=time)
        await ctx.reply(embed=discord.Embed(description=f"<:tick:966707201064464395> Slowmode set for **{time}s**",color=discord.Color.green()))

    @commands.Cog.listener()
    async def on_message(self,msg):
        if msg.channel.id == GENERAL:
            global msgss
            msgss+=1

#   THIS CHECKS IF THERE ARE MORE THAN 1 MESSAGE IN 3 SECONDS IN GENERAL, IF SO, IT SETS A SLOWMODE OF 2s

@tasks.loop(seconds=60) 
async def auto_slowmode(bot:discord.Bot):
    chl=bot.get_channel(GENERAL)
    global msgss
    global slom
    try:
        if msgss>=20 and slom==False:
            await chl.edit(slowmode_delay=2)
            await chl.send(embed=discord.Embed(description="I added slowmode of **2s** as chat is fast!",color=discord.Color.green()))
            slom=True
        elif msgss<=20 and slom==True:
            await chl.edit(slowmode_delay=0)    
            await chl.send(embed=discord.Embed(description="I removed slowmode! enjoy :)",color=discord.Color.green()))
            slom=False
        msgss=0
    except:pass

def setup(bot):
    bot.add_cog(Slowmode(bot))
    print("Cog loaded: Slowmode")