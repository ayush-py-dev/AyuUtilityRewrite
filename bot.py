from random import choice
from config import TOKEN
from config import GUILD_ID
import discord
import datetime
from datetime import datetime
import DiscordUtils
from discord.ext import commands, tasks
import time
import utils.helps as helps
import jishaku
import asyncio

bot = commands.Bot(command_prefix="+",intents=discord.Intents.all(), help_command=helps.CustomHelp(),allowed_mentions=discord.AllowedMentions(everyone=False,replied_user=False))
tracker = DiscordUtils.InviteTracker(bot)

"""Loading Extension"""

bot.load_extension("jishaku")
cogs = ['levels', 'afk', 'pins', 'avatar','custombot','info','giveaway','verify','forms','rtfm','code_exc','suggestion','slowmode','userhelp','warns','welcome','mods','reminder','economy','booster','automod','todo','selfroles','logs','tickets','psutil','banapp','rules','staff']
loaded_cogs=[]
for i in cogs:
    bot.load_extension(f"cogs.{i}")
    loaded_cogs.append(i)


""" ERROR HANDLER HERE """

@bot.event
async def on_command_error(ctx, error):
    embed = discord.Embed(description=":x: Error!", color=discord.Color.red())
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        embed.add_field(name="Missing Required Argument", value=f"```{error.args[0]}```")
        await ctx.reply(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed.add_field(name="Missing Permissions", value=f"```{error.args[0]}```")
        await ctx.reply(embed=embed)
    elif isinstance(error, commands.BotMissingPermissions):
        embed.add_field(name="Bot Missing Permissions", value=f"```{error.args[0]}```")
        await ctx.reply(embed=embed)
    elif isinstance(error, commands.CommandOnCooldown):
        embed.add_field(name="Command On Cooldown", value=f"```{error.args[0]}```")
        await ctx.reply(embed=embed)
    elif isinstance(error, commands.NotOwner):
        embed.add_field(name="Not Owner", value=f"```{error.args[0]}```")
        await ctx.reply(embed=embed)
    elif isinstance(error, commands.MissingRole):
        role = discord.utils.get(ctx.guild.roles, name=error.missing_role)
        embed.add_field(name="Missing Role", value=f"Role {role.mention} is required to use this command")
        await ctx.reply(embed=embed)
    elif isinstance(error, commands.MissingAnyRole):
        roles = [discord.utils.get(ctx.guild.roles, name=role) for role in error.missing_roles]
        embed.add_field(name="Missing Role", value=f"Roles {', '.join([role.mention for role in roles])} are required to use this command")
        await ctx.reply(embed=embed)
    else:
        embed.add_field(name="Terminal Error", value=f"```{error}```")
        await ctx.reply(embed=embed)
        raise error

@bot.event
async def on_application_command_error(ctx, error):
    embed = discord.Embed(description=":x: Error!", color=discord.Color.red())
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        embed.add_field(name="Missing Required Argument", value=f"```{error.args[0]}```")
        await ctx.respond(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed.add_field(name="Missing Permissions", value=f"```{error.args[0]}```")
        await ctx.respond(embed=embed)
    elif isinstance(error, commands.BotMissingPermissions):
        embed.add_field(name="Bot Missing Permissions", value=f"```{error.args[0]}```")
        await ctx.respond(embed=embed)
    elif isinstance(error, commands.CommandOnCooldown):
        embed.add_field(name="Command On Cooldown", value=f"```{error.args[0]}```")
        await ctx.respond(embed=embed)
    elif isinstance(error, commands.NotOwner):
        embed.add_field(name="Not Owner", value=f"```{error.args[0]}```")
        await ctx.respond(embed=embed)
    elif isinstance(error, commands.MissingRole):
        role = discord.utils.get(ctx.guild.roles, id=error.missing_role)
        embed.add_field(name="Missing Role", value=f"Role {role.mention} is required to use this command")
        await ctx.respond(embed=embed)
    elif isinstance(error, commands.MissingAnyRole):
        roles = [discord.utils.get(ctx.guild.roles, id=role) for role in error.missing_roles]
        embed.add_field(name="Missing Role", value=f"Roles {', '.join([role.mention for role in roles])} are required to use this command")
        await ctx.respond(embed=embed)
    else:
        embed.add_field(name="Terminal Error", value=f"```{error}```")
        await ctx.respond(embed=embed)
        raise error

@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name} with Id: {bot.user.id}\nPing Being: {round(bot.latency*1000)}ms")
    update_status.start(guild=bot.get_guild(GUILD_ID))


""""COMMANDS START FROM HERE"""

@bot.group(name="cog",help="Cog Based Commands",invoke_without_command=True)
@commands.is_owner()
async def cog(ctx):
    await ctx.reply(embed=discord.Embed(color=discord.Color.green(),description=", ".join(loaded_cogs)))

@cog.command(aliases=["ul"],name="unload",help="Unload cogs")
@commands.is_owner()
async def unload(ctx,cogss:str=None):
    if not cogss:
        for i in cogs:
            if i in loaded_cogs:
                bot.unload_extension(f"cogs.{i}")
                loaded_cogs.remove(i)
                await ctx.send(embed=discord.Embed(description=f"Unloaded {i}.py",color=discord.Color.green()))
    else:
        cogl=cogss.split(", ")
        for i in cogl:
            if i in loaded_cogs:
                bot.unload_extension(f"cogs.{i}")
                loaded_cogs.remove(i)
                await ctx.send(embed=discord.Embed(description=f"Unloaded {i}.py",color=discord.Color.green()))


@cog.command(aliases=["l"],name="load",help="Load cogs")
@commands.is_owner()
async def load(ctx,cogss:str=None):
    if not cogss:
        for i in cogs:
            if i not in loaded_cogs:
                bot.load_extension(f"cogs.{i}")
                loaded_cogs.append(i)
                await ctx.send(embed=discord.Embed(description=f"Loaded {i}.py",color=discord.Color.green()))
    else:
        cogl=cogss.split(", ")
        for i in cogl:
            if i not in loaded_cogs:
                bot.load_extension(f"cogs.{i}")
                loaded_cogs.append(i)
                await ctx.send(embed=discord.Embed(description=f"Loaded {i}.py",color=discord.Color.green()))

@cog.command(aliases=["rl","re"],name="reload",help="Reload cogs")
@commands.is_owner()
async def reload(ctx,cogss:str=None):
    if not cogss:
        for i in loaded_cogs:
            bot.reload_extension(f"cogs.{i}")
            await ctx.send(embed=discord.Embed(description=f"Reloaded {i}.py",color=discord.Color.green()))
    else:
        cogl=cogss.split(", ")
        for i in cogl:
            if i in loaded_cogs:
                bot.reload_extension(f"cogs.{i}")
                await ctx.send(embed=discord.Embed(description=f"Reloaded {i}.py",color=discord.Color.green()))


@bot.slash_command(name="ping",description="Calculate the latency of the bot")
async def ping(ctx):
    lats = []
    then = datetime.utcnow()
    embed = discord.Embed(color=discord.Color.green(), description=f"Pinging...")
    message = await ctx.respond(embed=embed)
    color = discord.Color.blurple()
    for i in range(5):    
        latency = round(bot.latency * 1000)
        lats.append(latency)
        if latency <= 110:
            color = discord.Color.green()
            emoji = "🟢"
        elif latency <= 115:
            color = discord.Color.gold()
            emoji = "🟡"
        else:
            color = discord.Color.red()
            emoji = "🔴"
        embed.add_field(name=f"Ping {i+1}", value=f"{emoji} {latency}ms",inline=False)
        embed.color = color
        await message.edit_original_message(embed = embed)
        await asyncio.sleep(0.5)
    now = datetime.utcnow()
    await asyncio.sleep(0.2)
    avg = round(sum(lats)/len(lats))
    diff = now - then
    em = discord.Embed(title=" ",
                       description="🏓 Pong!",
                       timestamp=datetime.utcnow(),
                       color=color
                       ).add_field(
        name="🕐 Bot's Latency:",
        value=f"{avg}ms",
        inline=True
    ).add_field(
        name="🔁 Calculation Time:",
        value=f"{round(diff.total_seconds() * 1000)}ms",
    )
    await message.edit_original_message(embed=em)

    
@tasks.loop(minutes=15)
async def update_status(guild: discord.Guild):
    names = choice(["Ayu","Tanishq","Amisha","Midnight"]) # Name of my friends
    statuses = ['over Ayu\'s Server', 'you', 'Ayu', '@everyone', 'general chat', 'discord', '+help', 'your mom',
                'Tanishq trolling Ayu', 'Ayu simp for Bot', 'new members', 'the staff team', 'helpers', 'code',
                'mass murders', f'{names} be an idiot', 'a video', 'watches', 'Ayu\'s Feet', 'fight club', 'youtube',
                'https://www.ayuitz.tech', 'potatoes', 'simps', 'people', 'my server', 'humans destroy the world',
                'AI take over the world', 'female bots 😳', 'dinosaurs', 'https://youtu.be/dQw4w9WgXcQ', 'idiots',
                'the beginning of WWIII', 'verified bot tags with envy',
                'Server Boosters (boost to get your name here)', 'OG members', "dalek rising from the ashes",
                'spongebob', 'turtles', 'SQUIRREL!!!', 'people get banned', 'por...k chops', 'my poggers discriminator',
                'tux', 'linux overcome windows', 'ayu get a gf', 'a documentary','ban appeals',
                'Tanishq fight for ownership','goats','coffee sips?','boosterssss','Ender Dragon','Ayu mining crypto','Coder\'s Mansion']
    
    status = choice(statuses)
    if status == 'boosterssss':
        boost_role = guild.get_role(852950166968991795)
        boost_count = guild.premium_subscription_count
        if boost_count == 0:
            status = "0 boost? ;-;" 
        else:
            booster = [member for member in guild.members if boost_role in member.roles]
            booster = choice(booster)
            status = f'{booster.name}! Thanks for boost..'
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))

if __name__ == "__main__":
    bot.run(TOKEN)
