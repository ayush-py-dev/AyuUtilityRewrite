from random import choice
from time import time
import discord
from discord.ext import commands
import aiosqlite
from config import LOGS


async def get_wid():
    db = await aiosqlite.connect("Database/warns.db")
    res = "welp"
    while res is not None:
        ink = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        inklist = []
        wid = "#"
        for i in ink:
            inklist.append(i)
        for i in range(5):
            let = choice(inklist)
            wid = f"{wid}{let}"
        cur = await db.execute("SELECT wid FROM warn WHERE wid=?", (wid,))
        res = await cur.fetchone()
    await db.close()
    return wid


async def createdb():
    db = await aiosqlite.connect("Database/warns.db")
    await db.execute("""
    CREATE TABLE IF NOT EXISTS warn(
        memid INTEGER,
        reason TEXT,
        mod INTEGER,
        time INTEGER,
        wid TEXT
    )
        """)
    await db.close()


class Warnings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def warndb(self, ctx):
        await createdb()
        await ctx.reply("warning db created!")

    @commands.command(
        name="warn",
        aliases=["w"]
    )
    @commands.has_role(1000072283282477158)
    async def warn(
        self,
        ctx: commands.Context,
        member: discord.Member,
        *,
        reason
    ):
        """
        Warn a member
        **Syntax:** +[warn|w] <member> <reason>
        """
        wid = await get_wid()
        db = await aiosqlite.connect("Database/warns.db")
        await db.execute(
            "INSERT INTO warn VALUES(?,?,?,?,?)",
            (
                member.id,
                reason,
                ctx.author.id,
                int(time()),
                wid
            )
        )
        await db.commit()
        await db.close()
        await ctx.reply(
            embed=discord.Embed(
                description=f"<:tick:966707201064464395> Warned: `{str(member)} `Reason: `{reason}`",
                color=discord.Color.green()
            )
        )
        try:
            await member.send(
                embed=discord.Embed(
                    description=f"You have been warned in {ctx.guild.name} for `{reason}`",
                    color=discord.Color.red()
                )
            )
        except:
            pass
        log_channel = self.bot.get_channel(LOGS)
        await log_channel.send(
            embed=discord.Embed(
                description=f"Warned: `{str(member)}`\nReason: `{reason}`\nModerator: `{ctx.author}`",
                color=discord.Color.red()
            )
        )

    @commands.command(
        aliases=["wn", "warns", "warning"]
    )
    @commands.has_role(
        1000072283282477158  # Staff role
    )
    async def warnings(self, ctx, member: discord.Member):
        """
        Shows the number of warnings a user has
        **Syntax:** +[warnings|wn|warns|warning] <member>
        """
        db = await aiosqlite.connect("Database/warns.db")
        cur = await db.execute("SELECT * FROM warn WHERE memid=? ORDER BY time DESC", (member.id,))
        res = await cur.fetchall()
        await db.close()
        if not res:
            return await ctx.reply(embed=discord.Embed(description=f"{member.mention} has **0** warnings", color=discord.Color.green()))
        embed = discord.Embed(
            description=f"{member.mention} warnings:", color=discord.Color.red())
        wc = 1
        for i in res:
            embed.add_field(
                name=f"Warn {wc}:",
                value=f"**Warned by:** <@{i[2]}> **for:** {i[1]} **on:** <t:{i[3]}:R> **Id:** `{i[4]}`",
                inline=False)
            wc += 1

        await ctx.send(embed=embed)

    @commands.command(name="clearwarn", aliases=["cw", "clear-warns", "clearwarns", "warn-clear"])
    @commands.has_permissions(manage_channels=True)
    async def clearwarn(self, ctx: commands.Context, member: discord.Member):
        """
        Clear all warnings of a user
        **Syntax:** +[clearwarn|cw|clear-warns|clearwarns|warn-clear] <member>
        """
        db = await aiosqlite.connect("Database/warns.db")
        try:
            await db.execute("DELETE FROM warn WHERE memid=?", (member.id,))
            await db.commit()
            await ctx.reply(embed=discord.Embed(description=f"Cleared warnings for: {member.mention}", color=discord.Color.green()))
            log_channel = self.bot.get_channel(LOGS)
            await log_channel.send(embed=discord.Embed(description=f"Warns cleared for: {member.mention}\nModerator: {ctx.author.mention}", color=discord.Color.red()))
        except:
            await ctx.reply(embed=discord.Embed(description=f"No warnings found for: **{member.mention}**", color=discord.Color.red()))
        await db.close()

    @commands.command(name="warn-delete", aliases=["wd", "warnd", "warnrem"])
    @commands.has_permissions(manage_channels=True)
    async def warn_delete(self, ctx, wid):
        """
        Delete a warning
        **Syntax:** +[warn-delete|wd|warnd|warnrem] <wid>
        """
        db = await aiosqlite.connect("Database/warns.db")
        try:
            await db.execute("DELETE FROM warn WHERE wid=?", (wid,))
            await db.commit()
            await ctx.reply(embed=discord.Embed(description=f"Deleted warn with id **{wid}**", color=discord.Color.green()))
            log_channel = self.bot.get_channel(LOGS)
            await log_channel.send(embed=discord.Embed(description=f"Warn deleted with id: **{wid}**\nModerator: {ctx.author.mention}", color=discord.Color.red()))
        except Exception as e:
            await ctx.reply(embed=discord.Embed(description=f"No warnings found with id: **{wid}**", color=discord.Color.red()))
        await db.close()


def setup(bot):
    bot.add_cog(Warnings(bot))
    print("Cog loaded: Warnings")
