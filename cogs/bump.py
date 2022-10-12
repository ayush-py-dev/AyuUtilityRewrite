from datetime import datetime

from time import time
import config

import discord
from discord.ext import commands, tasks

class Bump(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    """
    Check if the user has bumped the server using Disboard message
    """
    @commands.Cog.listener(name="on_ready")
    async def when_ready(self):
        await send_bump_message.start(
            self
        )

    @commands.Cog.listener(name="on_message")
    async def bump_handler(self, message: discord.Message):
        bump_role = message.guild.get_role(
            config.BUMPER_ROLE
        )

        author: discord.Member = await message.guild.fetch_member(
                message.author.id
            )


        if message.author.id == 302050872383242240 and "Bump done" in message.embeds[0].description and message.interaction:
            await message.delete(
                reason="Bump Message"
            )

            user: discord.Member = await message.guild.fetch_member(
                message.interaction.user.id
            )

            with open("bumper.txt", "w") as f:
                f.write(
                    f"{user.id}, {int(time()+(2*60*60))}, {message.channel.id}"
                )

            await user.add_roles(bump_role)

            embed = discord.Embed(
                description="Bump Done!\nThanks for bumping.\nYou have been given {0} role, it will boost your message xp gain by 20% for 2 hours.".format(
                    bump_role.mention
                ),
                color=discord.Color.og_blurple(),
                timestamp=datetime.utcnow()
            )

            await message.channel.send(
                content=user.mention,
                embed=embed
            )

            return

        if bump_role in author.roles:
            with open("bumper.txt", "r") as f:
                data = f.read().split(", ")
            if not author.id == int(data[0]):
                print("Not the same user")
                await author.remove_roles(bump_role)
                return

@tasks.loop(seconds=10)
async def send_bump_message(self):
    with open(
        "bumper.txt",
        "r"
    ) as f:
        content = f.read()
        in_list = content.split(
            ", "
        )
    try:
        if int(in_list[1]) <= int(time()):
            channel = await self.bot.get_channel(
                int(
                    in_list[2]
                )
            )
            await channel.send(
                embed=discord.Embed(
                    description="Bump Available Now.",
                    color=discord.Color.green()
                )
            )
            with open(
                "bumper.txt",
                "w"
            ) as f:
                f.write(
                    "000"
                )
    except IndexError:
        pass


def setup(bot: commands.Bot):
    bot.add_cog(Bump(bot))
    print("Cog Loaded: Bump")
