import random
import aiosqlite

import discord
from discord.ext import commands

import time
from config import GUILD_ID


class Afk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(guild_ids=[GUILD_ID], description="""Sets your afk""")
    @commands.cooldown(1, 10, commands.BucketType.member)
    @commands.has_any_role(1000072283282477158, 810893581174177813) # The staff role and level 40 role of my server
    async def afk(self, ctx: commands.Context, reason: str = None):
        reason = reason or "AFK"
        member = ctx.author
        db: aiosqlite.Connection = await aiosqlite.connect("Database/afk.db")
        cur = await db.execute("SELECT memres FROM afk WHERE memid=?", (member.id,))
        res = await cur.fetchone()
        if not res:
            await db.execute("INSERT INTO afk VALUES(?,?,?,?)", (member.id, member.display_name, reason, int(time.time())))
            await db.commit()
            try:
                await member.edit(nick=f"[AFK] {member.display_name}")
            except:
                pass
            emoji = random.choice(['⚪', '🔴', '🟤', '🟣', '🟢', '🟡', '🟠', '🔵'])
            em = discord.Embed(
                title=" ",
                description=f"{emoji} I set your AFK: {reason}",
                color=discord.Color.blue()
            )
            await ctx.respond(embed=em)
        elif res:
            em = discord.Embed(
                description=" You are already AFK",
                color=discord.Color.brand_red()
            )
            await ctx.respond(embed=em, ephemeral=True)
        await db.close()

    @commands.Cog.listener(name="on_message")
    async def check_afk_message(self, msg):
        if msg.author.bot or msg.guild is None:
            return
        elif msg.guild.id == GUILD_ID:
            db = await aiosqlite.connect("Database/afk.db")
            cur = await db.execute("SELECT memname FROM afk WHERE memid=?",
                 (msg.author.id,)
            )
            name = await cur.fetchone()
            if name:
                cur = await db.execute("SELECT afktime FROM afk WHERE memid=?",
                (msg.author.id,)
            )
                trs = await cur.fetchone()
                tp = int(time.time())-int(trs[0]) # checking the afk time
                if tp < 30:
                    pass # type: ignore
                else:
                    await db.execute("DELETE FROM afk WHERE memid=?",
                        (msg.author.id,)
                    )
                    await db.commit()
                    try:
                        await msg.author.edit(nick=f"{name[0]}")
                    except:
                        pass
                    emoji = random.choice(
                        ['<a:wokeup:938726418890760263>', '<:sleepy2:938727815241687080>', '<:sleepy1:938727830324387900>'])
                    em = discord.Embed(
                        description=f"{emoji} I removed your AFK",
                        color=discord.Color.dark_gold()
                    )
                    await msg.reply(embed = em)
            await db.close()
    
    @commands.Cog.listener(name="on_message")
    async def check_afk_mention(self, message: discord.Message):
        if not message.guild.id == GUILD_ID:
            return
        for mention in message.mentions:
            db : aiosqlite.Connection = await aiosqlite.connect("Database/afk.db")
            cursor = await db.execute("SELECT memres, afktime FROM afk WHERE memid = ?",
                (mention.id)
            )
            await db.close()
            result = await cursor.fetchone()
            if not result:
                return await db.close()
            emojies = random.choice( # NOTE: add your custom emojies here.
                [
                    '<a:emoji_3:938727345831960617>' ,
                    '<:in_sleep1:938727849429434399>'
                ]
            )
            embed = discord.Embed(
                description="{0} {1} is AFK: {2} ({3})".format(
                    emojies,
                    mention.mention ,
                    result[0],
                    f"<t:{result[1]}:>"
                )
            )
            await message.reply(embed = embed)
            break

def setup(bot):
    bot.add_cog(Afk(bot))
    print("Cog loaded: Afk")
