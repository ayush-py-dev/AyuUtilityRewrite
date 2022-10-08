import discord
from discord.ext import commands, tasks

from pytimeparse import parse
from config import *

import aiosqlite
from random import choice

import time


async def create_reminder_id():
    """
    Create a random reminder id
    """
    db=await aiosqlite.connect("Database/reminder.db")
    res="welp"
    while res is not None:
        ink="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        inklist=[]
        wid="#"
        for i in ink:inklist.append(i)
        for i in range(5):
            let=choice(inklist)
            wid=f"{wid}{let}"
        cur=await db.execute("SELECT reminder_id FROM reminder WHERE reminder_id=?",(wid,))
        res=await cur.fetchone()
    await db.close()
    return wid

def convert_time(time):
    """
    Convert a time string to seconds
    """
    return parse(time)

class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        """
        When the bot is ready
        """
        db = await aiosqlite.connect("Database/reminder.db")
        await db.execute("""
        CREATE TABLE IF NOT EXISTS reminder (
            user_id INTEGER,
            message TEXT,
            time INTEGER,
            channel_id INTEGER,
            reminder_id INTEGER
        )
        """)
        await db.commit()
        await db.close()
        await reminder_task.start(self.bot)

    @commands.slash_command(
        guild_ids=[GUILD_ID],
        description="""Remind yourself of something"""
    )
    async def remind(
        self,
        ctx, times, message):
        time_in_sec = convert_time(times)
        if not time_in_sec:
            return await ctx.respond(
                "Invalid time format",
                ephemeral=True
            )
        epoch = time_in_sec+int(time.time())
        db = await aiosqlite.connect("Database/reminder.db")
        _id = await create_reminder_id()
        await db.execute("INSERT INTO reminder VALUES(?,?,?,?,?)", (ctx.author.id, message, epoch, ctx.channel.id,_id))
        await db.commit()
        await db.close()
        await ctx.respond(
            f"I will remind you <t:{epoch}:R> : {message}"
        )
        

    @commands.slash_command(
        guild_ids=[GUILD_ID],
        name="reminders",
        description="""Get all your reminders"""
    )
    async def reminders(
        self,
        ctx: commands.Context
    ):
        db = await aiosqlite.connect("Database/reminder.db")
        cur = await db.execute("SELECT * FROM reminder WHERE user_id=?", (ctx.author.id,))
        reminders = await cur.fetchall()
        await db.close()
        if not reminders:
            return await ctx.respond(
                "You have no reminders",
                ephemeral=True
            )
        embed = discord.Embed(
            title="Your reminders"
        )
        for reminder in reminders:
            embed.add_field(
                name=f"Reminder ID: {reminder[4]}",
                value=f"Message: {reminder[1]} Time: <t:{reminder[2]}:R>",
                inline=False
            )
        await ctx.respond(
            embed=embed
        )

    @commands.slash_command(
        guild_ids=[GUILD_ID],
        description="""Delete a reminder"""
    )
    async def delete_reminder(
        self,
        ctx: commands.Context,
        reminder_id: str
    ):
        db = await aiosqlite.connect("Database/reminder.db")
        cur = await db.execute(
            "SELECT * FROM reminder WHERE user_id=? AND reminder_id=?",
            (
                ctx.author.id,
                reminder_id
            )
        )
        reminder = await cur.fetchone()
        if not reminder:
            return await ctx.respond(
                "You have no reminders with that id",
                ephemeral=True
            )
        await db.execute(
            "DELETE FROM reminder WHERE user_id=? AND reminder_id=?",
            (
                ctx.author.id,
                reminder_id
            )
        )
        await db.commit()
        await db.close()
        await ctx.respond(f"Deleted reminder: {reminder[1]}",ephemeral=True)
    
    @commands.command(guild_ids=[GUILD_ID], description="""Clear all your reminders""")
    async def clear_reminders(self, ctx):
        db = await aiosqlite.connect("Database/reminder.db")
        await db.execute(
            "DELETE FROM reminder WHERE user_id=?",
            (
                ctx.author.id,
            )
        )
        await db.commit()
        await db.close()
        await ctx.respond(
            "Cleared all your reminders",
            ephemeral=True
        )

@tasks.loop(
    seconds=10 # this is directly propotional to resource consumption and indirectly to accuracy
)
async def reminder_task(
    bot:commands.Bot
):
    db = await aiosqlite.connect('Database/reminder.db')
    cursor = await db.execute(
        "SELECT * FROM reminder WHERE time<=?",
        (
            int(
                time.time()
            ),
        )
    )
    reminders = await cursor.fetchall()
    for reminder in reminders:
        user = bot.get_user(reminder[0])
        try:
            await user.send(
                f"Reminder: {reminder[1]}"
            )
        except discord.Forbidden:
            await bot.get_channel(
                reminder[3]).send(
                    f"{user.mention},you told me to remind: {reminder[1]} (<t:{reminder[2]}:R>)"
                )
        await db.execute(
            "DELETE FROM reminder WHERE time=?",
            (
                reminder[2],
            )
        )
    await db.commit()
    await db.close()

def setup(bot):
    bot.add_cog(Reminder(bot))
    print("Cog loaded: Reminder")