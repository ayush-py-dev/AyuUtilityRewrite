from discord.ext import commands
import discord
from config import *
import asyncio
# from discord.ui import Button, View

class CustomBot(commands.Cog):
    def __init__(self,bot: commands.Bot):
        self.bot=bot
    

    @commands.slash_command(
        guild_ids=[GUILD_ID],
        description="Add your custom bot"
    )
    @commands.has_any_role(
        BOTROLE,
        1000072283282477158 # staff role
    )
    @commands.cooldown(
        1,
        60,
        commands.BucketType.user
    )
    async def addbot(self,ctx: commands.Context):
        await ctx.respond(
            "You have requested to add your bot to the server.\nWrite `confirm` to begin"
        )
        def check(msg):
            return msg.author==ctx.author and msg.channel==ctx.channel
        try:
            msg=await self.bot.wait_for(
                'message',
                check=check,
                timeout=10.0
            )
        except TimeoutError:
            await ctx.respond(
                "Timeout!\nTry again later."
            )
        else:
            await msg.delete()
            if msg.content.lower()=="confirm":
                em=discord.Embed(
                    title=" ",
                    description="You have started bot submission\nPlease answer the questions asked below.",
                    color=discord.Color.random()
                )
                botmsg=await ctx.send(
                    embed=em
                )
                await asyncio.sleep(
                    2.5
                )
                em=discord.Embed(
                    title="<a:listening:942447554275201077> Q1.",
                    description="Enter Bot Id",
                    color=discord.Color.random()
                )
                await botmsg.edit(
                    content=None,
                    embed=em
                )
                try:
                    botid=await self.bot.wait_for(
                        'message',
                        check=check,
                        timeout=30
                    )
                except TimeoutError:
                    await ctx.respond("Timeout!\nTry again later.")
                else:
                    await botid.delete()
                    botid=botid.content
                    bott=await self.bot.fetch_user(int(botid))
                    if not bott.bot: # if the user is not a bot
                        await botmsg.edit(
                            content=None,
                            embed=discord.Embed(
                                title=" ",
                                description="The user is not a bot",
                                color=discord.Color.red()
                            )
                        )
                        return
                    em=discord.Embed(
                        title=" ",
                        description="Please confirm by writing `yes` if this is your bot.",
                        color=discord.Color.random()
                    ).set_author(
                        name=f"{bott.name}#{bott.discriminator}",
                        icon_url=bott.display_avatar
                    ).set_thumbnail(
                        url=bott.display_avatar
                    )
                    await botmsg.edit(
                        content=None,
                        embed=em
                    )
                    try:
                        conf=await self.bot.wait_for('message',check=check,timeout=10.0)
                    except TimeoutError:
                        await ctx.respond("Timeout!\nTry again later.")
                    else:
                        await conf.delete()
                        if conf.content.lower()=="yes":
                            quest=["Why you want to add this bot in this server?",
                                "What is the prefix of your bot?",
                                "Does it contains slash commands?",
                                "How many server your bot is in?",
                                "What are the features of your bot?",
                            ]
                            ans=[]
                            qn=2
                            for q in quest:
                                em=discord.Embed(
                                    title=f"<a:listening:942447554275201077> Q{qn}",
                                    description=f"{q}",
                                    color=discord.Color.random()
                                )
                                await botmsg.edit(
                                    content=None,
                                    embed=em
                                )
                                try:
                                    an=await self.bot.wait_for(
                                        'message',
                                        check=check,
                                        timeout=60.0
                                    )
                                except TimeoutError:
                                    await ctx.respond("Timeout!\nTry again later.")
                                else:
                                    await an.delete()
                                    ans.append(str(an.content))
                                    qn+=1
                            
                            em=discord.Embed(
                                title="Bot Submission",
                                description="A new bot submission request have been made!\nClick on its name to invite it to the server!",
                                color=discord.Color.random()
                            )
                            em.set_author(
                                name=f"{bott.name}#{bott.discriminator}",
                                icon_url=bott.display_avatar,
                                url=f"https://discord.com/oauth2/authorize?client_id={bott.id}&scope=bot&guild_id={ctx.guild.id}"
                            ).add_field(
                                name="Bot Id:",
                                value=f"{bott.id}",
                                inline=True
                            ).add_field(
                                name="Submitted by:",
                                value=f"{ctx.author.mention}({str(ctx.author)})",
                            )
                            ansc=0
                            for q in quest:
                                em.add_field(
                                    name=f"{q}",
                                    value=f"{ans[ansc]}",
                                    inline=True
                                )
                                ansc+=1
                            
                            em.set_footer(
                                text=f"{ctx.author.name}#{ctx.author.discriminator}",
                                icon_url=ctx.author.display_avatar
                            )
                            subc=self.bot.get_channel(BOTFORMSUBCHANNEL)
                            await subc.send(embed=em)
                            cem=discord.Embed(
                                title=" ",
                                description="<:success:942446821987450992> We have successfully submitted your request,\nwe will inform you when we add the bot"
                            )
                            await botmsg.edit(
                                content=None,
                                embed=cem
                            )
                        else:
                            await ctx.respond(
                                "Submission Cancelled!",
                                ephemeral=True
                            )
            else:
                await ctx.respond(
                    "Submission Cancelled!",
                    ephemeral=True
                )
                            

def setup(bot):
    bot.add_cog(CustomBot(bot))