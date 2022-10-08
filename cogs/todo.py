from ast import alias
import discord
from discord.ext import commands

import aiosqlite
import time

from random import choice

async def get_todoid():
    db=await aiosqlite.connect("Database/todo.db")
    res="welp"
    while res is not None:
        ink="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        inklist=[]
        wid="#"
        for i in ink:inklist.append(i)
        for i in range(5):
            let=choice(inklist)
            wid=f"{wid}{let}"
        cur=await db.execute("SELECT todo_id FROM todo WHERE todo_id=?",(wid,))
        res=await cur.fetchone()
    await db.close()
    return wid

class Todo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = None
    
    """
    A cog to handle todo list
    """

    @commands.Cog.listener()
    async def on_ready(self):
        self.db = await aiosqlite.connect('Database/todo.db')
        await self.db.execute("""CREATE TABLE IF NOT EXISTS todo (
            member_id INTEGER,
            todo TEXT,
            created_at INTEGER,
            todo_id TEXT
        )""")
        await self.db.commit()
    
    @commands.group(name="todo",invoke_without_command=True,aliases=["td"])
    async def todo(self,ctx):
        """
        A utility to handle todo list
        """
        await ctx.send(
            embed=discord.Embed(
                color=discord.Color.green(),
                description="""
        **Todo**
        +`[todo|td] [add|ad|a] <todo>` - Add a todo
        +`[todo|td] [list|ls|l]` - List all todos
        +`[todo|td] [remove|rm|r] <id>` - Remove a todo
        +`[todo|td] [clear|cls|clr|cl|c]` - Clear all todos
        """
        )
    )
    
    @todo.command(
        name="add",
        help="Add a todo",
        aliases=["a","ad"]
    )
    @commands.cooldown(
        2,
        10,
        commands.BucketType.user
    )
    async def add(
        self,
        ctx: commands.Context,
        *,
    todo:str):
        """
        Add a todo
        **Syntax:** +[todo|td] [add|ad|a] <todo>
        """
        todo_id = await get_todoid()
        await self.db.execute(
            """INSERT INTO todo VALUES(?,?,?,?)""",
            (
                ctx.author.id,
                todo,
                int(time.time()),
                todo_id
            )
        )
        await self.db.commit()
        await ctx.send(
            embed=discord.Embed(
                color=discord.Color.green(),
                description=f"Added `{todo}` to todo list"
            )
        )

    @todo.command(name="list",help="List all todos",aliases=["l","ls"])
    async def list(
        self,
        ctx: commands.Context
    ):
        """
        List all todos
        **Syntax:** +[todo|td] [list|ls|l]
        """
        cur = await self.db.execute(
            """SELECT * FROM todo WHERE member_id=?""",
            (
                ctx.author.id,
            )
        )
        res = await cur.fetchall()
        if not res:
            await ctx.send(
                embed=discord.Embed(
                    color=discord.Color.red(),
                    description="No todos found"
                )
            )
        else:
            desc = ""
            for i in res:
                desc += f"<a:arrow_arrow:993887543873507328> {i[1]} (<t:{i[2]}:R>) `id: {i[3]}`\n\n"
            await ctx.send(
                embed=discord.Embed(
                    color=discord.Color.green(),
                    description=desc,
                    title=f"{str(ctx.author)}'s Todo List."
                )
            )
    
    @todo.command(
        name="remove",
        help="Remove a todo",aliases=["r","rm"])
    async def remove(
        self,
        ctx: commands.Context,
        *,
        todo_id:str
    ):
        """
        Remove an item from todo list
        **Syntax:** +[todo|td] [remove|r|rm] <id>
        """
        todo_id = "#"+todo_id
        cur = await self.db.execute(
            """SELECT * FROM todo WHERE member_id=? AND todo_id=?""",
            (
                ctx.author.
                id,todo_id
            )
        )
        res = await cur.fetchone()
        if not res:
            await ctx.send(
                embed=discord.Embed(
                    color=discord.Color.red(),
                    description="No item found from id `{}` in your todo list".format(todo_id)
                )
            )
        else:
            await self.db.execute(
                """DELETE FROM todo WHERE member_id=? AND todo_id=?""",
                (
                    ctx.author.id,
                    todo_id
                )
            )
            await self.db.commit()
            await ctx.send(
                embed=discord.Embed(
                    color=discord.Color.green(),
                    description=f"Removed `{res[1]}` from todo list"
                )
            )
    
    @todo.command(
        name="clear",
        help="Clear all todos",
        aliases=["c","cl","cls","clr"]
    )
    async def clear(
        self,
        ctx: commands.Context
    ):
        """
        Clear all items from todo list
        **Syntax:** +[todo|td] [clear|cls|clr|cl|c]
        """
        await self.db.execute(
            """DELETE FROM todo WHERE member_id=?""",
            (
                ctx.author.id,
            )
        )
        await self.db.commit()
        await ctx.send(
            embed=discord.Embed(
                color=discord.Color.green(),
                description="Cleared all todos"
            )
        )

def setup(bot):
    bot.add_cog(Todo(bot))
    print("Cog loaded: Todo")