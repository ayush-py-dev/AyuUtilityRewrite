from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import random
import discord
from discord.ext import commands
from config import *
from datetime import datetime

class VeriyView(discord.ui.View):
	def __init__(self,bott):
		super().__init__(timeout=None)
		self.bott=bott
	
	@discord.ui.button(
		label="Verify",
		emoji="<a:done:942447861075968000>",
		custom_id="VerifyBtn",
		style=discord.ButtonStyle.green
	)
	async def verifybtn(
		self,
		button,
		interaction
	):
		r = interaction.guild.get_role(VERIFY_ROLE)
		await interaction.user.add_roles(r)
		await interaction.response.send_message(
			f"Verified {interaction.user.mention}"
			,ephemeral=True
		)
		emb = discord.Embed(
			title="Verification Log",
			description="Verified {0}#{1}".format(
				interaction.user.name,
				interaction.user.discriminator),
			timestamp=datetime.utcnow(),
			color=discord.Color.dark_theme()
		).set_footer(
		    text=f"id: {interaction.user.id}",
			icon_url=interaction.user.display_avatar
		)
		lch = self.bott.get_channel(LOGS)
		await lch.send(embed=emb)



class Verify(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
		self.bot.verify_view = False
		

	@commands.Cog.listener()
	async def on_ready(self):
		if self.bot.verify_view is False:
			self.bot.add_view(VeriyView(self.bot))
			self.bot.verify_view=True

	@commands.command(
		guild_ids=[GUILD_ID],
		description="""Verify yourself"""
	)
	@commands.is_owner()
	async def verify(self,ctx):
		# await ctx.message.delete()
		await ctx.send(
			embed=discord.Embed(
				description="Verify to gain access to server",
				color=discord.Color.green()),
			view=VeriyView(
				self.bot
			)
		)




def setup(bot):
	bot.add_cog(Verify(bot))
	print("Cog Loaded: Verify")