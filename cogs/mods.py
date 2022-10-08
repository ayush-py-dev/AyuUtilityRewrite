import datetime
import discord
from discord.ext import commands

import time
from pytimeparse import parse
from config import *


def time_in_epoch(time_string):
    time_in_secs = parse(time_string)
    return int(time_in_secs+time.time())


def convert(times):
    if times.isdigit():
        return int(times)
    else:
        time_in_secs = parse(times)
        return datetime.timedelta(seconds=time_in_secs)


class Mods(commands.Cog):
    """
    A cog to handle all the moderation commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="kick",
        help="Kick a user from the server"
    )
    @commands.has_permissions(
        kick_members=True
    )
    async def kick(
        self,
        ctx, member: discord.Member,
        *,
        reason: str = None
    ):
        """
        Kick a user from the server
        **Syntax**: +[kick] <user> <reason>
        """
        reason = reason or "No reason provided"
        if member == ctx.author:
            await ctx.send(
                embed=discord.Embed(
                    description="You can't kick yourself",
                    color=discord.Color.red()
                )
            )
        elif member.top_role >= ctx.author.top_role:
            await ctx.send(
                embed=discord.Embed(
                    description="You can't kick a user with a higher role than you",
                    color=discord.Color.red()
                )
            )
        else:
            await member.kick(reason=f"Kicked by {str(ctx.author)}: {reason}")
            await ctx.send(
                embed=discord.Embed(
                    description=f"Kicked {member.mention}",
                    color=discord.Color.green()
                )
            )
            log_channel = self.bot.get_channel(LOGS)
            await log_channel.send(
                embed=discord.Embed(
                    description=f"Kicked {member.mention} by {ctx.author.mention} for {reason}",
                    color=discord.Color.green()
                )
            )

    @commands.command(
        name="ban",
        help="Ban a user from the server"
    )
    @commands.has_permissions(
        ban_members=True
    )
    async def ban(
        self,
        ctx: commands.Context,
        member: discord.Member,
        *,
        reason: str = None
    ):
        """
        Ban a user from the server
        **Syntax**: +[ban] <user> <reason>
        """
        reason = reason or "No reason provided"
        if member == ctx.author:
            await ctx.send(
                embed=discord.Embed(
                    description="You can't ban yourself",
                    color=discord.Color.red()
                )
            )
        elif member.top_role >= ctx.author.top_role:
            await ctx.send(
                embed=discord.Embed(
                    description="You can't ban a user with a higher role than you",
                    color=discord.Color.red()
                )
            )
        else:
            await member.ban(
                reason=f"Banned by {str(ctx.author)}: {reason}"
            )
            await ctx.send(
                embed=discord.Embed(
                    description=f"Banned {member.mention}",
                    color=discord.Color.green()
                )
            )
            log_channel = self.bot.get_channel(LOGS)
            await log_channel.send(
                embed=discord.Embed(
                    description=f"Banned {member.mention} by {ctx.author.mention} for {reason}",
                    color=discord.Color.green()
                )
            )

    @commands.command(
        name="unban",
        help="Unban a user from the server"
    )
    @commands.has_permissions(
        ban_members=True
    )
    async def unban(
        self,
        ctx: commands.Context,
        *,
        member: discord.User
    ):
        """
        Unban a user from the server
        **Syntax**: +[unban] <user>
        """
        await ctx.guild.unban(member)
        await ctx.send(
            embed=discord.Embed(
                description=f"Unbanned {member.mention}",
                color=discord.Color.green()
            )
        )
        log_channel = self.bot.get_channel(LOGS)
        await log_channel.send(
            embed=discord.Embed(
                description=f"Unbanned {member.mention} by {ctx.author.mention}",
                color=discord.Color.green()
            )
        )

    @commands.command(name="purge", help="Purge a number of messages from the channel")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, *, amount: int = None):
        """
        Purge a number of messages from the channel
        **Syntax**: +[purge] <amount>
        """
        amount = amount or 1
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(
            embed=discord.Embed(
                description=f"Purged {amount} messages",
                color=discord.Color.green()
            ),
            delete_after=3
        )
        log_channel = self.bot.get_channel(LOGS)
        await log_channel.send(
            embed=discord.Embed(
                description=f"Purged {amount} messages by {ctx.author.mention} in {ctx.channel}",
                color=discord.Color.green()
            )
        )

    @commands.command(
        name="mute"
    )
    @commands.has_permissions(
        mute_members=True
    )
    async def mute(
        self,
        ctx: commands.Context,
        member: discord.Member,
        ttime: str,
        *,
        reason: str = None
    ):
        """
        Mute a member
        **Syntax**: +[mute] <user> "<time>" <reason>
        """
        if member == ctx.author:
            await ctx.send(
                embed=discord.Embed(
                    description="You can't mute yourself",
                    color=discord.Color.red()
                )
            )
            return
        elif member.top_role >= ctx.author.top_role:
            await ctx.send(
                embed=discord.Embed(
                    description="You can't mute a user with a higher role than you",
                    color=discord.Color.red()
                )
            )
            return
        reason = reason or "No reason provided"
        time_left = time_in_epoch(ttime)
        duration = convert(ttime)
        if duration:
            until: datetime.datetime = discord.utils.utcnow() + duration
            await member.timeout(
                until=until,
                reason=f"Muted by {str(ctx.author)}: {reason}"
            )
            await ctx.send(
                embed=discord.Embed(
                    description=f"Muted {member.mention} until <t:{time_left}:F>",
                    color=discord.Color.green()
                )
            )
            log_channel = self.bot.get_channel(LOGS)
            await log_channel.send(
                embed=discord.Embed(
                    description=f"Muted {member.mention} by {ctx.author.mention}\nReason: {reason}\nUntil: <t:{time_left}:R>",
                    color=discord.Color.green()
                )
            )
        else:
            await ctx.send(
                embed=discord.Embed(
                    description="Please provide a valid time",
                    color=discord.Color.red()
                )
            )

    @commands.command(
        name="unmute",
    )
    @commands.has_permissions(
        manage_messages=True
    )
    async def unmute(self, ctx, member: discord.Member):
        """
        Unmute a member
        **Syntax**: +[unmute] <user>
        """
        if member == ctx.author:
            await ctx.send(
                embed=discord.Embed(
                    description="You can't unmute yourself",
                    color=discord.Color.red()
                )
            )
            return
        elif member.top_role >= ctx.author.top_role:
            await ctx.send(
                embed=discord.Embed(
                    description="You can't unmute a user with a higher role than you",
                    color=discord.Color.red()
                )
            )
            return
        await member.timeout(
            until=None,
            reason=f"Unmuted by {str(ctx.author)}"
        )
        await ctx.send(
            embed=discord.Embed(
                description=f"Unmuted {member.mention}",
                color=discord.Color.green()
            )
        )
        log_channel = self.bot.get_channel(LOGS)
        await log_channel.send(
            embed=discord.Embed(
                description=f"Unmuted {member.mention} by {ctx.author.mention}",
                color=discord.Color.green()
            )
        )

    @commands.command(
        name="nick",
    )
    @commands.has_permissions(
        manage_nicknames=True
    )
    async def nick(
        self,
        ctx: commands.Context,
        member: discord.Member,
        *,
        nickname: str = None
    ):
        """
        Change a user's nickname
        **Syntax**: +[nick] <user> <nickname>
        """
        await member.edit(
            nick=nickname
        )
        await ctx.send(
            embed=discord.Embed(
                description=f"Changed {member.mention}'s nickname to {nickname}",
                color=discord.Color.green()
            )
        )
        log_channel = self.bot.get_channel(LOGS)
        await log_channel.send(
            embed=discord.Embed(
                description=f"Changed {member.mention}'s nickname to {nickname} by {ctx.author.mention}",
                color=discord.Color.green()
            )
        )

    @commands.command(
        name="revive",
    )
    @commands.cooldown(
        1,
        10*60,  # 60s * 10s = 600s = 10 minute
        commands.BucketType.user
    )
    async def revive(self, ctx: commands.Context):
        """
        Ping Revive Role
        **Syntax**: +[revive]
        """
        if not ctx.author.guild_permissions.manage_messages:
            return await ctx.reply("https://tenor.com/8coi.gif")
        revive_role = ctx.guild.get_role(REVIVE_ROLE)
        log_channel = self.bot.get_channel(LOGS)
        await log_channel.send(
            embed=discord.Embed(
                description=f"{ctx.author.mention} pinged {revive_role.mention}",
                color=discord.Color.green()
            )
        )
        em = discord.Embed(
            description=f"{ctx.author.mention} revived the chat!",
            color=discord.Color.green()
        )
        await ctx.message.delete()
        msg = await ctx.send(revive_role.mention)
        await msg.edit(
            content=None,
            embed=em
        )

    @commands.command(
        name="role",
        help="Add or Remove role to a user"
    )
    @commands.has_permissions(
        administrator=True
    )
    async def role(
        self,
        ctx: commands.Context,
        member: discord.Member,
        *,
        role: discord.Role
    ):
        """
        Add or Remove role to a user
        **Syntax**: +[role] <user> <role>
        """
        if role in member.roles:
            await member.remove_roles(role)
            await ctx.reply(
                embed=discord.Embed(
                    description=f"Removed {role.mention} from {member.mention}",
                    color=discord.Color.green()
                )
            )
            log_channel = self.bot.get_channel(LOGS)
            await log_channel.send(
                embed=discord.Embed(
                    description=f"Removed {role.mention} from {member.mention} by {ctx.author.mention}",
                    color=discord.Color.green()
                ),
                allowed_mentions=None
            )
        else:
            await member.add_roles(role)
            await ctx.reply(
                embed=discord.Embed(
                    description=f"Added {role.mention} to {member.mention}",
                    color=discord.Color.green()
                )
            )
            log_channel = self.bot.get_channel(LOGS)
            await log_channel.send(
                embed=discord.Embed(
                    description=f"Added {role.mention} to {member.mention} by {ctx.author.mention}",
                    color=discord.Color.green()
                ),
                allowed_mentions=None
            )


def setup(bot):
    bot.add_cog(Mods(bot))
    print("Cog Loaded: Mods")
