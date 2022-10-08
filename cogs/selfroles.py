import discord
from discord.ext import commands

"""
These are self roles... you need to highly modify it elsewise it'll not work for your server
"""


class RolesView(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        super().__init__(timeout=None)

    """
    Give roles on button reaction
    """

    @discord.ui.button(label="18+", custom_id="age18pbutton", style=discord.ButtonStyle.blurple, emoji="<a:18p:997892181052358696>", row=0)
    async def p18(self, button: discord.Button, interaction: discord.Interaction):
        role = interaction.guild.get_role(809985304211488808)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(embed=discord.Embed(description=f"Removed {role.mention} role", color=discord.Color.red()), ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(embed=discord.Embed(description=f"Added {role.mention} role", color=discord.Color.green()), ephemeral=True)

    @discord.ui.button(label="18-", custom_id="age18mbutton", style=discord.ButtonStyle.blurple, emoji="<a:18m:997892202401366056>:", row=0)
    async def m18(self, button: discord.Button, interaction: discord.Interaction):
        role = interaction.guild.get_role(809985552312565781)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(embed=discord.Embed(description=f"Removed {role.mention} role", color=discord.Color.red()), ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(embed=discord.Embed(description=f"Added {role.mention} role", color=discord.Color.green()), ephemeral=True)

    @discord.ui.button(label="Male", custom_id="gendermale", style=discord.ButtonStyle.blurple, emoji="<a:Male:997896650955694210>", row=1)
    async def genm(self, button: discord.Button, interaction: discord.Interaction):
        role = interaction.guild.get_role(809985079282499594)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(embed=discord.Embed(description=f"Removed {role.mention} role", color=discord.Color.red()), ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(embed=discord.Embed(description=f"Added {role.mention} role", color=discord.Color.green()), ephemeral=True)

    @discord.ui.button(label="Female", custom_id="genderfemale", style=discord.ButtonStyle.blurple, emoji="<a:Female:997896655670087701>", row=1)
    async def genf(self, button: discord.Button, interaction: discord.Interaction):
        role = interaction.guild.get_role(809985239773872138)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(embed=discord.Embed(description=f"Removed {role.mention} role", color=discord.Color.red()), ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(embed=discord.Embed(description=f"Added {role.mention} role", color=discord.Color.green()), ephemeral=True)

    @discord.ui.button(label="Non-Binary", custom_id="gendernonbin", style=discord.ButtonStyle.blurple, emoji="<:NonBinary:1000042393967542344>", row=1)
    async def gennb(self, button: discord.Button, interaction: discord.Interaction):
        role = interaction.guild.get_role(1003320420730146896)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(embed=discord.Embed(description=f"Removed {role.mention} role", color=discord.Color.red()), ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(embed=discord.Embed(description=f"Added {role.mention} role", color=discord.Color.green()), ephemeral=True)

    @discord.ui.button(label="Chat Revival", custom_id="pingchat", style=discord.ButtonStyle.red, emoji="<:PING:1000429429954187264>", row=2)
    async def chatping(self, button: discord.Button, interaction: discord.Interaction):
        role = interaction.guild.get_role(810132068150673420)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(embed=discord.Embed(description=f"Removed {role.mention} role", color=discord.Color.red()), ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(embed=discord.Embed(description=f"Added {role.mention} role", color=discord.Color.green()), ephemeral=True)

    @discord.ui.button(label="Announcements", custom_id="pingann", style=discord.ButtonStyle.red, emoji="<:PING:1000429429954187264>", row=2)
    async def announcping(self, button: discord.Button, interaction: discord.Interaction):
        role = interaction.guild.get_role(810131991080992788)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(embed=discord.Embed(description=f"Removed {role.mention} role", color=discord.Color.red()), ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(embed=discord.Embed(description=f"Added {role.mention} role", color=discord.Color.green()), ephemeral=True)

    @discord.ui.button(label="Partnership", custom_id="pingpart", style=discord.ButtonStyle.red, emoji="<:PING:1000429429954187264>", row=2)
    async def partnerping(self, button: discord.Button, interaction: discord.Interaction):
        role = interaction.guild.get_role(812302524966371349)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(embed=discord.Embed(description=f"Removed {role.mention} role", color=discord.Color.red()), ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(embed=discord.Embed(description=f"Added {role.mention} role", color=discord.Color.green()), ephemeral=True)

    @discord.ui.button(label="Poll", custom_id="pingpoll", style=discord.ButtonStyle.red, emoji="<:PING:1000429429954187264>", row=2)
    async def pollping(self, button: discord.Button, interaction: discord.Interaction):
        role = interaction.guild.get_role(810131946587291668)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(embed=discord.Embed(description=f"Removed {role.mention} role", color=discord.Color.red()), ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(embed=discord.Embed(description=f"Added {role.mention} role", color=discord.Color.green()), ephemeral=True)

    @discord.ui.button(label="Question of the Day", custom_id="pingqotd", style=discord.ButtonStyle.red, emoji="<:PING:1000429429954187264>", row=2)
    async def qotdping(self, button: discord.Button, interaction: discord.Interaction):
        role = interaction.guild.get_role(810131877616812062)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(embed=discord.Embed(description=f"Removed {role.mention} role", color=discord.Color.red()), ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(embed=discord.Embed(description=f"Added {role.mention} role", color=discord.Color.green()), ephemeral=True)


class SelfRoles(commands.Cog):
    """
    A cog made for users to get roles with the help of buttons
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.roleview = False

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.roleview:
            self.bot.add_view(RolesView(self.bot))
            self.roleview = True

    @commands.command()
    @commands.is_owner()
    async def selfrole(self, ctx: commands.Context):
        """
        Sends role buttons
        """
        embed = discord.Embed(
            description="Click the buttons to get roles!", color=discord.Color.blue())
        embed.set_author(name="SelfRoles",
                         icon_url=self.bot.user.display_avatar)

        await ctx.send(embed=embed, view=RolesView(self.bot))


def setup(bot):
    bot.add_cog(SelfRoles(bot))
    print("Cog Loaded: SelfRoles")
