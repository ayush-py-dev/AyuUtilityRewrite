from operator import is_
import discord
from discord.ext import commands

import aiosqlite

from config import *

"""
You probably don't need this cog...
"""

class Staff(commands.Cog):
    """
    A group of commands for tracking the staff records of the server.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(name="strike")
    @commands.has_permissions(administrator=True)
    async def strike(self, ctx: commands.Context, member: discord.Member):
        """
        Strike a Staff
        """
        db : aiosqlite.Connection = await aiosqlite.connect("Database/staff.db")
        cur = await db.execute("SELECT strike FROM staff WHERE memid=?", (member.id,))
        res = await cur.fetchone()
        if not res:
            await db.close()
            return await ctx.reply(embed=discord.Embed(description="This user is not a staff member.", color=discord.Color.red()))
        await db.execute("UPDATE staff SET strike=? WHERE memid=?", (res[0] + 1, member.id))
        await db.commit()
        await db.close()
        await ctx.reply(embed=discord.Embed(description=f"{member.mention} has been striked.\nThey have {res[0]+1} strike now.", color=discord.Color.green()))
    
    @commands.command(name="unstrike")
    @commands.has_permissions(administrator=True)
    async def unstrike(self, ctx: commands.Context, member: discord.Member):
        """
        Unstrike a Staff
        """
        db : aiosqlite.Connection = await aiosqlite.connect("Database/staff.db")
        cur = await db.execute("SELECT strike FROM staff WHERE memid=?", (member.id,))
        res = await cur.fetchone()
        if not res:
            await db.close()
            return await ctx.reply(embed=discord.Embed(description="This user is not a staff member.", color=discord.Color.red()))
        await db.execute("UPDATE staff SET strike=? WHERE memid=?", (res[0] - 1, member.id))
        await db.commit()
        await db.close()
        await ctx.reply(embed=discord.Embed(description=f"{member.mention} has been unstriked.\nThey have {res[0]-1} strike now.", color=discord.Color.green()))
    
    @commands.command(name="update-staff-db")
    @commands.has_permissions(administrator=True)
    async def update_staff(self, ctx: commands.Context):
        """
        Update the staff database and show the changes.
        """
        db : aiosqlite.Connection = await aiosqlite.connect("Database/staff.db")
        await db.execute("DELETE FROM staff")
        staff_role = ctx.guild.get_role(1000072283282477158)
        for member in ctx.guild.members:
            if staff_role in member.roles:
                await db.execute("INSERT INTO staff VALUES (?, ?)", (member.id, 0))
        await db.commit()
        await db.close()
        await ctx.reply(embed=discord.Embed(description="The staff database has been updated.", color=discord.Color.green()))
    
    @commands.command(name="show-staff-db")
    @commands.has_permissions(administrator=True)
    async def show_staff(self, ctx: commands.Context):
        """
        Show the staff database.
        """
        async def get_all_in_string():
            db : aiosqlite.Connection = await aiosqlite.connect("Database/staff.db")
            cur = await db.execute("SELECT * FROM staff")
            res = await cur.fetchall()
            await db.close()
            header = "Staff - Strike"
            lists = "\n".join([f"{self.bot.get_user(i[0]).mention} - {i[1]}" for i in res])
            return f"{header}\n{lists}"
        await ctx.reply(embed=discord.Embed(description=await get_all_in_string(), color=discord.Color.green()))
    
    @commands.command(name="strikes")
    @commands.has_permissions(administrator=True)
    async def strikes(self, ctx: commands.Context, member: discord.Member):
        """
        Get the strikes of a staff member
        """
        db : aiosqlite.Connection = await aiosqlite.connect("Database/staff.db")
        cur = await db.execute("SELECT strike FROM staff WHERE memid=?", (member.id,))
        res = await cur.fetchone()
        if not res:
            await db.close()
            return await ctx.reply(embed=discord.Embed(description="This user is not a staff member.", color=discord.Color.red()))
        await db.close()
        await ctx.reply(embed=discord.Embed(description=f"{member.mention} has {res[0]} strikes.", color=discord.Color.green()))

    @commands.command(name="update-staff-list")
    @commands.has_permissions(administrator=True)
    async def update_staff_list(self, ctx: commands.Context):
        """
        Update the staff list
        """
        # roles = {
        #     809642412535971882 : "Ayu",
        #     810108284073017384 : "Creator",
        #     809744895350407168 : "Adminstrator",
        #     809756163214147665 : "Head Moderator",
        #     983229059259588608 : "Senior Moderator",
        #     809756162962620448 : "Moderator",
        #     809756164019322890 : "Trial Moderator",
        #     919243964647895071 : "Offical Helper"
        # }
        def get_staff_count(role_id: int):
            return len([member for member in ctx.guild.members if ctx.guild.get_role(role_id) in member.roles])
        
        staff_role = ctx.guild.get_role(1000072283282477158)
        count = get_staff_count(staff_role.id)
        ayu, ayu_role = get_staff_count(809642412535971882), ctx.guild.get_role(809642412535971882)
        creator, creator_role = get_staff_count(810108284073017384), ctx.guild.get_role(810108284073017384)
        admin, admin_role = get_staff_count(809744895350407168), ctx.guild.get_role(809744895350407168)
        head_mod, head_mod_role = get_staff_count(809756163214147665), ctx.guild.get_role(809756163214147665)
        senior_mod, senior_mod_role = get_staff_count(983229059259588608), ctx.guild.get_role(983229059259588608)
        mod, mod_role = get_staff_count(809756162962620448), ctx.guild.get_role(809756162962620448)
        trial_mod, trial_mod_role = get_staff_count(809756164019322890), ctx.guild.get_role(809756164019322890)
        helper, helper_role = get_staff_count(919243964647895071), ctx.guild.get_role(919243964647895071)

        embed = discord.Embed(title="Staff List", description=f"Total Staff: {count}", color=discord.Color.embed_background())
        def create_value(member: discord.Member):
            return f"> `{member.id}` {member.mention}"
        def get_all_staff(role_id: int):
            return "\n".join([create_value(member) for member in ctx.guild.members if ctx.guild.get_role(role_id) in member.roles])
        embed.add_field(name="** **",value=f"{ayu_role.mention} | **{ayu}**\n\n{get_all_staff(809642412535971882)}", inline=False)
        embed.add_field(name="** **",value=f"{creator_role.mention} | **{creator}**\n\n{get_all_staff(810108284073017384)}", inline=False)
        embed.add_field(name="** **",value=f"{admin_role.mention} | **{admin}**\n\n{get_all_staff(809744895350407168)}", inline=False)
        embed.add_field(name="** **",value=f"{head_mod_role.mention} | **{head_mod}**\n\n{get_all_staff(809756163214147665)}", inline=False)
        embed.add_field(name="** **",value=f"{senior_mod_role.mention} | **{senior_mod}**\n\n{get_all_staff(983229059259588608)}", inline=False)
        embed.add_field(name="** **",value=f"{mod_role.mention} | **{mod}**\n\n{get_all_staff(809756162962620448)}", inline=False)
        embed.add_field(name="** **",value=f"{trial_mod_role.mention} | **{trial_mod}**\n\n{get_all_staff(809756164019322890)}", inline=False)
        embed.add_field(name="** **",value=f"{helper_role.mention} | **{helper}**\n\n{get_all_staff(919243964647895071)}", inline=False)
        staff_list_channel = ctx.guild.get_channel(983610422412337172)
        await staff_list_channel.edit(topic=f"Total Staff: {count}")
        await staff_list_channel.purge(limit=5)
        await staff_list_channel.send(embed=embed)
        await ctx.reply(embed=discord.Embed(description="The staff list has been updated.", color=discord.Color.green()))

def setup(bot):
    bot.add_cog(Staff(bot))
    print("Cog loaded: Staff")
            