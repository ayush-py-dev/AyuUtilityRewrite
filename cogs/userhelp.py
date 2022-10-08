import asyncio
from datetime import datetime
import discord
from discord.ext import commands
from discord.ui import Modal, InputText

class UserHelpModal(Modal):
    def __init__(self,title,bot,msg:discord.Message):
        super().__init__(title=title)

        self.bot=bot
        self.msg = msg
        self.add_item(
            InputText(
            label="Language",
            value="Python",
            placeholder="Write your language",
            required=True,
            style=discord.InputTextStyle.short
            ))
        
        self.add_item(
            InputText(
            label="Topic",
            placeholder="Write your topic for help.",
            required=True,
            style=discord.InputTextStyle.singleline,
            max_length=20
            ))
    

        self.add_item(
            InputText(
                label="Details",
                style=discord.InputTextStyle.long,
                placeholder="Give a meaningful and sufficient points on your problem",
                required=True,
                min_length=20
            ))
        self.add_item(
            InputText(
                label="Code",
                style=discord.InputTextStyle.paragraph,
                placeholder="Paste code, if any also wrap it in ```lang ```",
                required=False,
                max_length=1990
            ))   
        self.add_item(
            InputText(
                label="Errors",
                style=discord.InputTextStyle.paragraph,
                placeholder="Paste error, if any also wrap it in ```lang ```",
                required=False,
                max_length=1990
            ))
        
        
    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(color=discord.Color.random(),timestamp=datetime.utcnow()
        ).set_author(
            name=str(interaction.user),icon_url=interaction.user.avatar.url
        ).add_field(
            name="Language:", value=self.children[0].value, inline=False
        ).add_field(
            name="Topic:", value=self.children[1].value, inline=False
        ).add_field(
            name="Description:", value=self.children[2].value, inline=False
        )
        await interaction.response.send_message("Join thread to get help!",ephemeral=True)
        msg=await interaction.channel.send(embed=embed)
        await interaction.channel.send(embed=discord.Embed(description="Get Help by clicking the button below!",color=discord.Color.og_blurple()),view=UserHelpBtn(self.bot))
        thread = await msg.create_thread(
            name=self.children[1].value
        )
        await self.msg.delete()
        await thread.send(
            interaction.user.mention,
            embed=discord.Embed(
                description="Our helpers will be here soon!\nPlease don't ping anyone.",
                color=discord.Color.blurple()
            )
        )
        await thread.send(
            f"Code:\n{self.children[3].value}"
        )
        await thread.send(
            f"Error:\n{self.children[4].value}"
        )


class UserHelpBtn(discord.ui.View):
    def __init__(self,bot):
        self.bot=bot
        super().__init__(timeout=None)
    
    @discord.ui.button(
        label="Get Help",
        custom_id="UserHelpButton",
        style=discord.ButtonStyle.blurple,
        emoji="<:developer:942447062476288050>"
    )
    async def gethelp(
        self,
        button,
        interaction:discord.Interaction
    ):
        msg = interaction.message
        modal=UserHelpModal(
            title="Help!!!",
            bot=self.bot,
            msg=msg
        )
        await interaction.response.send_modal(modal)

class UserHelp(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.bot.helping_view = False

    
    @commands.Cog.listener()
    async def on_ready(self):
        if self.bot.helping_view is False:
            self.bot.add_view(UserHelpBtn(self.bot))
            self.bot.helping_view=True


    @commands.command()
    @commands.is_owner()
    async def userhelp(self,ctx):
        await ctx.message.delete()
        await ctx.send(
            embed=discord.Embed(
                description="Get Help by clicking the button below!",
                color=discord.Color.og_blurple()
            ),
            view=UserHelpBtn(
                self.bot
            )
        )

def setup(bot):
    bot.add_cog(UserHelp(bot))
    print("Cog Loaded: UserHelp")