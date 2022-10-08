from ast import alias
from operator import inv
import discord
from discord.ext import commands

class Rules(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    """
    A cog to handle all the rules synced with TCM's rules
    """

    @commands.group(
        invoke_without_command=True,
        aliases=["rule"]
    )
    async def rules(
        self,
        ctx:commands.Context
    ):
        embed = discord.Embed(
            description="You can read server rules here: <#809642447646883840>",
            color = discord.Color.dark_theme()
        )
        await ctx.reply(
            embed=embed
        )
    
    @rules.command(
        name="1"
    )
    async def rule1(
        self,
        ctx:commands.Context
    ):
        embed = discord.Embed(
            title="Rule 1",
            description="No nsfw in any channel",
            color = discord.Color.dark_theme()
        )
        embed.add_field(
            name="What is NSFW?",
            value="NSFW stands for Not Safe For Work. It is content that is not suitable for work or school. This includes mature/poronography/gore/violence and other disturbing content.",
            inline=False
        )
        embed.add_field(
            name="Detail:",
            value="You are not allowed to send any NSFW messages in any channel in this server.",
            inline=False
        )

        await ctx.reply(embed=embed)
    
    @rules.command(
        name="2"
    )
    async def rule2(
        self,
        ctx: commands.Context
    ):
        embed = discord.Embed(title="Rule 2", description="No Impersonation", color = discord.Color.dark_theme())
        embed.add_field(name="What is Impersonation?", value="Impersonation is pretending to be someone else. This includes using someone else's name, avatar, or other identifying information.",inline=False)
        embed.add_field(name="Detail:",value="You are not allowed to impersonate anyone in this server.",inline=False)

        await ctx.reply(embed=embed)
    
    @rules.command(name="3")
    async def rule3(self, ctx):
        embed = discord.Embed(title="Rule 3",description="Follow Discord ToS and Community Guidelines", color = discord.Color.dark_theme())
        embed.add_field(name="What is Discord ToS and Community Guidelines?", value="Discord Terms of Service and Community Guidelines are the rules that you must follow to use Discord. You can read them here: https://discord.com/terms and https://discord.com/guidelines",inline=False)
        embed.add_field(name="Detail:",value="You are not allowed to break Discord ToS and Community Guidelines in this server.",inline=False)

        await ctx.reply(embed=embed)
    
    @rules.command(name="4")
    async def rule4(self, ctx):
        embed = discord.Embed(title="Rule 4",description="Respect others and their belongings", color = discord.Color.dark_theme())
        embed.add_field(name="What is Respect?", value="Respect is treating others with kindness and consideration. This includes not being rude, mean, or offensive to others.",inline=False)
        embed.add_field(name="Detail:",value="You are not allowed to be rude, mean, or offensive to others in this server.",inline=False)

        await ctx.reply(embed=embed)
    
    @rules.command(name="5")
    async def rule5(self, ctx):
        embed = discord.Embed(title="Rule 5",description="No spamming", color = discord.Color.dark_theme())
        embed.add_field(name="What is Spamming?", value="Spamming is sending the same message multiple times in a row.",inline=False)
        embed.add_field(name="Detail:",value="You are not allowed to spam in this server.",inline=False)

        await ctx.reply(embed=embed)

    @rules.command(name="6")
    async def rule6(self, ctx):
        embed = discord.Embed(title="Rule 6",description="No Politics and Controversial topics", color = discord.Color.dark_theme())
        embed.add_field(name="What is Politics and Controversial topics?", value="Politics and Controversial topics are topics that are controversial or political in nature. This includes politics, religion, and other controversial topics.",inline=False)
        embed.add_field(name="Detail:",value="You are not allowed to talk about politics and controversial topics in this server.",inline=False)

        await ctx.reply(embed=embed)
    
    @rules.command(name="7")
    async def rule7(self, ctx):
        embed = discord.Embed(title="Rule 7",description="No illegal activities", color = discord.Color.dark_theme())
        embed.add_field(name="What is illegal activities?", value="Illegal activities are activities that are illegal in your country. This includes illegal drugs, hacking, and other illegal activities.",inline=False)
        embed.add_field(name="Detail:",value="You are not allowed to do illegal activities in this server.",inline=False)

        await ctx.reply(embed=embed)
    
    @rules.command(name="8")
    async def rule8(self, ctx):
        embed = discord.Embed(title="Rule 8",description="No begging", color = discord.Color.dark_theme())
        embed.add_field(name="What is begging?", value="Begging is asking for money, items, nitro or other things from others.",inline=False)
        embed.add_field(name="Detail:",value="You are not allowed to beg in this server.",inline=False)

        await ctx.reply(embed=embed)
    
    @rules.command(name="9")
    async def rule9(self, ctx):
        embed = discord.Embed(title="Rule 9",description="No advertising", color = discord.Color.dark_theme())
        embed.add_field(name="What is advertising?", value="Advertising is promoting your server, product, or other things.",inline=False)
        embed.add_field(name="Detail:",value="You are not allowed to advertise in this server.",inline=False)

        await ctx.reply(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Rules(bot))
    print("Cog loaded: Rules")