from re import I
from urllib import response
import discord
from discord.ext import commands, tasks

import aiohttp
from config import BAN_CHANNEL, BAN_LOGIN, BAN_PASSWORD

class BanView(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label="Unban", custom_id="unban", style=discord.ButtonStyle.green)
    async def unban(self, button: discord.Button, interaction: discord.Interaction):
        async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(login=BAN_LOGIN,
                password=BAN_PASSWORD,
                encoding="utf-8")
            ) as session:
            embed = interaction.message.embeds[0]
            user: discord.User = self.bot.get_user(
                int(embed.description)
            )
            await session.delete(url="https://ayuitz.deta.dev/appeal/?discord_id={}".format(
                embed.description
                )
            )
            try:
                await interaction.guild.unban(user,
                reason="Unbanned by {}".format(
                    interaction.user)
                )
            except:
                await interaction.response.send_message(embed=discord.Embed(
                    title="User already Unbaned!",
                    color=discord.Color.yellow()),
                    ephemeral=True)
                embed.color = discord.Color.yellow()
                embed.set_footer(
                    text=f"Not in Ban List"
                )
                await interaction.message.edit(embed=embed,
                    view=None
                )
            else:
                await interaction.response.send_message(embed=discord.Embed(
                    title="Unbanned",
                    description=f"**{user}** has been unbanned",
                    color=discord.Color.green()),
                    ephemeral=True
                )
                embed.color = discord.Color.green()
                embed.set_footer(text="Unbanned by {}".format(
                    interaction.user),
                    icon_url=interaction.user.display_avatar
                )
                await interaction.message.edit(embed=embed, view=None)

    @discord.ui.button(label="Reject", custom_id="reject", style=discord.ButtonStyle.red)
    async def delete(self, button: discord.Button, interaction: discord.Interaction):
        async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(login=BAN_LOGIN,
                password=BAN_PASSWORD,
                encoding="utf-8")
            ) as session:
            embed = interaction.message.embeds[0]
            user: discord.User = self.bot.get_user(int(embed.description))
            await session.delete(url="https://ayuitz.deta.dev/appeal/?discord_id={}".format(embed.description))
            await interaction.response.send_message(embed=discord.Embed(title="Rejected",
                description="Appeal has been deleted",
                color=discord.Color.red()),
                ephemeral=True
            )
            embed.color = discord.Color.red()
            embed.set_footer(
                text="Rejected by {}".format(
                interaction.user),
                icon_url=interaction.user.display_avatar)
            await interaction.message.edit(
                embed=embed,
                view=None
            )

    @discord.ui.button(label="Block", custom_id="block", style=discord.ButtonStyle.blurple)
    async def block(self, button: discord.Button, interaction: discord.Interaction):
        embed = interaction.message.embeds[0]
        embed.color = discord.Color.blurple()
        embed.set_footer(
            text=f"Blocked by: {interaction.user}",
            icon_url=interaction.user.display_avatar
        )
        await interaction.message.edit(
            embed=embed,
            view=None
        )
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Blocked",
                description="Appeal has been blocked",
                color=discord.Color.blurple()
            ),
            ephemeral=True
        )


class BanApp(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.banbutton = False

    """
    A cog to send ban appeal message
    """

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.banbutton:
            self.bot.add_view(BanView(self.bot))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id == BAN_CHANNEL:
            if message.webhook_id:
                await message.delete()
                embed = message.embeds[0]
                try:
                    user: discord.User = await self.bot.fetch_user(int(embed.description))
                except:
                    async with aiohttp.ClientSession(auth=aiohttp.BasicAuth(
                        login=BAN_LOGIN,
                        password=BAN_PASSWORD,
                        encoding="utf-8")
                    ) as session:
                        await session.delete(
                            url="https://ayuitz.deta.dev/appeal/?discord_id={}".format(
                                embed.description)
                            )
                else:
                    embed.set_author(
                        name=f"{user}",
                        icon_url=user.display_avatar
                    )
                    embed.color = discord.Color.darker_grey()
                    await message.channel.send(
                        embed=embed,
                        view=BanView(self.bot)
                    )


def setup(bot: commands.Bot):
    bot.add_cog(BanApp(bot))
    print("Cog Loaded: BanApp")
