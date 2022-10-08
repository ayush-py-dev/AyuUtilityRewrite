"""
Will soon add this with buttons.
"""

import discord
from discord.ext import commands, tasks
import aiosqlite
from config import *
from datetime import datetime
import time
import random
from pytimeparse import parse


def convert(time):
    time_in_sec = parse(time)
    if not time_in_sec:
        return 1000
    return time_in_sec


class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        giveawaycheck.start(self)

    @commands.slash_command(guild_ids=[GUILD_ID], description="""Start a giveaway""")
    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.has_role(GROLE)
    async def gstart(self, ctx):
        """
        Start a giveaway
        **Syntax**: `/gstart`
        """
        quest = [
            "Which channel should giveaway be hosted in?",
            "How long should the giveaway last?",
            "How many winners should be there in giveaway?(1-10)",
            "What should be the prize of the giveaway?"
        ]

        em = discord.Embed(
            title=" ",
            description="Answer the questions within 30s to start the giveaway!",
            timestamp=datetime.utcnow(),
            color=discord.Color.blurple()
        )

        await ctx.respond(embed=em)
        qmsg = await ctx.send(
            "Fetching Questions..."
        )
        ans = []

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        qc = 1
        for i in quest:
            em = discord.Embed(
                title=f"<a:listening:942447554275201077> Q{str(qc)}",
                description=f"{i}",
                color=discord.Colour.random()
            )
            qc += 1
            await qmsg.edit(
                content=None,
                embed=em
            )
            try:
                amsg = await self.bot.wait_for(
                    'message',
                    check=check,
                    timeout=30.0
                )
            except TimeoutError:
                await ctx.respond("Timeout, be quicker next time.")
            else:
                ans.append(amsg.content)
                await amsg.delete()

        em = discord.Embed(
            title=" ",
            description="Please confirm the given details",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        ).add_field(
            name=f"{quest[0]}",
            value=f"{ans[0]}",
            inline=False).add_field(
            name=f"{quest[1]}",
            value=f"{ans[1]}").add_field(
            name=f"{quest[2]}",
            value=f"{ans[2]}",
            inline=False).add_field(
            name=f"{quest[3]}",
            value=f"{ans[3]}")

        await qmsg.edit(
            content=None,
            embed=em
        )
        await qmsg.add_reaction(
            "<:success:942446821987450992>"
        )

        def reactcheck(react, user):
            return user == ctx.author and str(react.emoji) == "<:success:942446821987450992>"
        try:
            react, user = await self.bot.wait_for(
                'reaction_add',
                check=reactcheck,
                timeout=30.0
            )
        except TimeoutError:
            em = discord.Embed(
                title="Giveaway Cancelled!",
                description="No reaction was added!",
                color=discord.Color.red(),
                timestamp=datetime.utcnow()
            )

            await qmsg.edit(
                content=None,
                embed=em
            )
        else:
            cid = int(ans[0][2:-1])
            endtime = convert(ans[1])
            endtime = int(time.time())+int(endtime)
            gch = self.bot.get_channel(cid)
            em = discord.Embed(
                title="Giveaway Started!",
                description=f"Giveaway Started in {gch.mention}, it will end <t:{str(endtime)}:R>",
                color=discord.Color.green(),
                timestamp=datetime.utcnow())

            emg = discord.Embed(
                title="New Giveaway!",
                description="React with <a:tada:943909208926068827> to participate!",
                color=discord.Color.blurple(),
                timestamp=datetime.utcnow()
            ).add_field(
                name="Hosted by:",
                value=f"{ctx.author.mention}"
            ).add_field(
                name="Prize:",
                value=f"{ans[3]}"
            ).add_field(
                name="No of winners:",
                value=f"{str(ans[2])}").add_field(
                name="Ends at:",
                value=f"<t:{str(endtime)}:R>")
            gping = ctx.guild.get_role(GPING)

            gmsg = await gch.send(content=f"{gping.mention}", embed=emg)
            await gmsg.add_reaction("<a:tada:943909208926068827>")

            db = await aiosqlite.connect("Database/gaway.db")
            cur = await db.execute("INSERT INTO main VALUES(?,?,?,?,?,?)", (ctx.author.id, int(ans[2]), str(ans[3]), int(endtime), int(gmsg.id), int(cid)))
            await db.commit()
            await db.close()
            await ctx.respond(embed=em)


@tasks.loop(seconds=5)
async def giveawaycheck(self):
    db = await aiosqlite.connect("Database/gaway.db")
    cur = await db.execute("SELECT * FROM main WHERE ending<?", (int(time.time()),))
    res = await cur.fetchone()
    # print(res)
    if not res:
        return
    # print(i)
    gch = self.bot.get_channel(int(res[5]))
    gmsg = await gch.fetch_message(int(res[4]))
    prize = res[2]
    host = gmsg.guild.get_member(int(res[0]))
    no_of_winner = int(res[1])
    winners = await gmsg.reactions[0].users().flatten()
    winners.pop(winners.index(self.bot.user))
    winni = []
    for w in winners:
        wee = random.choice(winners)
        winners.pop(winners.index(wee))
        winni.append(wee.id)

    if len(winni) < no_of_winner:
        valid = False
    else:
        winner_role = gmsg.guild.get_role(853552328840970280)
        valid = True
    em = discord.Embed(
        title="Giveaway Ended!",
        description=f"Hosted by: {host.mention}",
        color=discord.Color.blurple(),
        timestamp=datetime.utcnow()
    ).add_field(
        name="Prize:",
        value=f"{prize}")

    if valid is True:
        em.add_field(
            name="Winners:",
            value=f"{', '.join([gmsg.guild.get_member(w).mention for w in winni])}")
        for w in winni:
            winner = gmsg.guild.get_member(w)
            await winner.add_roles(winner_role)

    else:
        em.add_field(
            name="Sad Life ;-;",
            value="Not enough reactions to choose winners!")

    await gmsg.reply(f"{winner_role.mention} Congrats!", embed=em)

    await db.execute("DELETE FROM main WHERE gmsgid=?", (int(res[4]),))
    await db.commit()

    await db.close()


def setup(bot):
    bot.add_cog(Giveaway(bot))
    print("Cog loaded: Giveaway")
