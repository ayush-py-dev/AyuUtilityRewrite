import asyncio
from time import time
import discord
import os
from discord.ext import commands
from config import *
from datetime import datetime
import chat_exporter
from github import Github


def upload_file(file_path: str, file_name: str, member_name: str):
    with open(f"{file_path}", "rb") as f:
        content = f.read()
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo("ayush-py-dev/ayuitztech") # it's a private repo you can't access it lol
    repo.create_file(
        path=f"ticket-logs/{file_name}.html",
        message=f"{member_name}",
        content=content,
        branch="main"
    )
    return file_name

class TrashButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(
        style=discord.ButtonStyle.red,
        emoji="🗑",
        label="Trash",
        custom_id="TrashButton"
    )
    async def trash(self,button,interaction):
        button.disabled=True
        button.label="Deleting"
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(
            embed=discord.Embed(
                description="<:tick:966707201064464395> Deleting ticket in **5s**",
                color=discord.Color.green()
            )
        )
        await asyncio.sleep(5)
        await interaction.channel.delete()

class CloseButton(discord.ui.View):
    def __init__(self,bott: commands.Bot):
        self.bott=bott
        super().__init__(timeout=None)
    
    @discord.ui.button(
        style=discord.ButtonStyle.red,
        emoji="🔒",
        label="Close",
        custom_id="CloseBtn"
    )
    async def close(self,button,interaction):
        button.disabled=True
        button.label="Closed!"
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("Closing Ticket...")
        

        categ=discord.utils.get(
            interaction.guild.categories,
            id=TICKETCATEGCLOSE
        )

        ch=interaction.channel
        r1=interaction.guild.get_role(TICKETROLE1)

        overwrite={
            interaction.guild.default_role:discord.PermissionOverwrite(read_messages=False),
            r1:discord.PermissionOverwrite(read_messages=True)
            }

        em=discord.Embed(
            description="Delete Ticket",
            color=discord.Color.dark_orange()
        )
        await ch.edit(
            category=categ,
            overwrites=overwrite
        )
        await ch.send(
            embed=em,
            view=TrashButton()
        )

        logch=self.bott.get_channel(
            TICKETLOGS
        )

        mem=await interaction.guild.fetch_member(int(ch.topic))
        export = await chat_exporter.export(ch)
        text=open(
            f"asset/ticket_logs/{mem.id}.html","a"
        )
        text.write(export)
        text.close()

        close_time = upload_file(
            f"asset/ticket_logs/{mem.id}.html",
            int(time()),
            mem.name
        )
        os.remove(
            f"asset/ticket_logs/{mem.id}.html"
        )

        em=discord.Embed(
            title="Ticket Logs!",
            color=discord.Color.random(),
            description=f"{mem.mention}'s ticket has been closed!",
            timestamp=datetime.utcnow()
        ).add_field(
            name="Closed By",
            value=f"{interaction.user.mention}"
        ).add_field(
            name="Closed",
            value=f"<t:{close_time}:R>"
        ).add_field(
            name="Transcript",
            value=f"[click here](https://ayuitz.tech/ticket-logs/{close_time})"
        )

        await logch.send(embed=em)
        
        

class CreateButton(discord.ui.View):
    def __init__(self,bott):
        self.bott=bott
        super().__init__(timeout=None)

    @discord.ui.button(
        style=discord.ButtonStyle.blurple,
        emoji="🎫",
        label="Click Here!",
        custom_id="TicketBtn"
    )
    async def tick(
        self,
        button: discord.ui.Button,
        interaction: discord.Interaction
    ):
        categ=discord.utils.get(
            interaction.guild.categories,
            id=TICKETCATEGOPEN
        )
        for ch in categ.channels:
            if ch.topic==str(interaction.user.id):
                return await ch.send(f"{interaction.user.mention} You already have a ticket here!")
        r1=interaction.guild.get_role(TICKETROLE1)
        overwrite={
            interaction.guild.default_role:discord.PermissionOverwrite(read_messages=False),
            interaction.user:discord.PermissionOverwrite(read_messages=True),
            r1:discord.PermissionOverwrite(read_messages=True)
            }
        channel=await categ.create_text_channel(
            name=f"{interaction.user.name}-{interaction.user.discriminator}",
            overwrites=overwrite,
            topic=f"{interaction.user.id}"
        ) # creating the channel/ticket
        em=discord.Embed(title="Welcome!",
                            description=f"Support will arrive shortly,\nmake sure not to ping anyone.\nFor fast support make sure\nto drop your question before hand.",
                            timestamp=datetime.utcnow(),
                            color=discord.Color.dark_blue()
                        ).set_author(
                            name=str(
                                interaction.user
                            ),
                            icon_url=interaction.user.display_avatar
                        )

        await interaction.response.send_message(
            f"{channel.mention} click to go to ticket",
            ephemeral=True
        )
        await channel.send(
            content=f"{r1.mention}",
            embed=em,
            view=CloseButton(self.bott)
        )

    

class Ticket(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.bot.persistent_views_added = False
    
    @commands.Cog.listener()
    async def on_ready(self):
        if self.bot.persistent_views_added is False:
            self.bot.add_view(TrashButton())
            self.bot.add_view(CreateButton(self.bot))
            self.bot.add_view(CloseButton(self.bot))
            self.bot.persistent_views_added=True
    
    @commands.command()
    @commands.is_owner()
    async def new(self,ctx):
        await ctx.message.delete()
        em=discord.Embed(
            title="Open a Ticket!",
            description="Creating a ticket for invalid reason will get you warned.\nIf you need any help regarding punishments,\nroles, or you just have a general question,\nfeel free to create a ticket and a\nstaff member will get to you shortly!\n**__Do not open support tickets for Coding Help.\nDoing so will get you warned.__**",
            color=0xffffff
        )

        await ctx.send(
            "Tickets 🎫",
            embed=em,
            view=CreateButton(self.bot)
        )
    
    @commands.command(name="add")
    @commands.has_role(TICKETROLE1)
    async def add(self,ctx: commands.Context,member:discord.Member):
        if ctx.channel.category.id!=TICKETCATEGOPEN:
            return await ctx.send(
                embed=discord.Embed(
                    description="This command can only be used in a ticket channel!",
                    color=discord.Color.red()
                )
            )
        await ctx.channel.set_permissions(
            member,
            read_messages=True,
            send_messages=True
        )
        await ctx.send(
            embed=discord.Embed(
                description=f"{member.mention} has been added to the ticket!",
                color=discord.Color.green()
            )
        )

    @commands.command(name="remove")
    @commands.has_role(TICKETROLE1)
    async def remove(self,ctx,member:discord.Member):
        if ctx.channel.category.id!=TICKETCATEGOPEN:
            return await ctx.send(embed=discord.Embed(description="This command can only be used in a ticket channel!",color=discord.Color.red()))
        await ctx.channel.set_permissions(member,read_messages=False,send_messages=False)
        await ctx.send(
            embed=discord.Embed(
                description=f"{member.mention} has been removed from the ticket!",
                color=discord.Color.green()
            )
        )
    

def setup(bot):
    bot.add_cog(Ticket(bot))
    print("Cog Loaded: Tickets")