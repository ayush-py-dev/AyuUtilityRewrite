import discord
from discord.ext import commands

class Boosters(commands.Cog):
    """
    A category to thank server boosters when they boost the server.
    """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after: discord.Member):
        # role: discord.Role = after.guild.premium_subscriber_role <- # NOTE: this will work for every server
        role = after.guild.get_role(852950166968991795)
        if role in after.roles and not role in before.roles:
            em=discord.Embed(
                description=f"<a:boost:983636359686279168> Thank you for boosting **{after.guild.name}**!\n\n",
                color=discord.Color.nitro_pink()
            ).add_field(
                name="** **",
                value="We are at **{}** boosts!".format(after.guild.premium_subscription_count),
            ).add_field(
                name="** **",
                value="We are boost level: **{}**".format(after.guild.premium_tier),
            ).set_thumbnail(
                url="https://c.tenor.com/HIqZKBb8sHgAAAAi/discord-boost-yellow-boost.gif"
            )
            await after.guild.system_channel.send(
                content=f"{after.mention}",
                embed=em
            )

def setup(bot):
    bot.add_cog(Boosters(bot))
    print("Cog loaded: Boosters")