import discord
from discord.ext import commands
from config import *
from datetime import datetime


class SelectBtn(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__(
            timeout=None
        )

    @discord.ui.button(
        label="Accept",
        style=discord.ButtonStyle.green,
        custom_id="Saccept"
    )
    async def accept(self,
                     button: discord.Button,
                     interaction: discord.Interaction
                     ):
        msg = interaction.message.content
        mem = await interaction.guild.fetch_member(int(msg))
        role = interaction.guild.get_role(TRIALMOD)
        await mem.add_roles(role)
        for i in self.children:
            i.disabled = True

        await interaction.response.edit_message(view=self)

        await interaction.followup.send(
            embed=discord.Embed(
                description=f"<:tick:966707201064464395> Selected {mem.mention} as a staff.\nThey have been added in Trial Period",
                color=discord.Color.green())
        )
        try:
            await mem.send(
                embed=discord.Embed(
                    description="<:tick:966707201064464395> You have been selected as staff!",
                    color=discord.Color.green()
                )
            )
        except discord.Forbidden:
            await interaction.followup.send(
                    embed=discord.Embed(
                    description="Unable to dm them",
                    color=discord.Color.red()
                )
            )

    @discord.ui.button(
        label="Deny",
        style=discord.ButtonStyle.red,
        custom_id="Sdeny"
    )
    async def deny(self,
        button: discord.Button,
        interaction: discord.Interaction
    ):
        for i in self.children:
            i.disabled = True
        await interaction.response.edit_message(view=self)

        msg = interaction.message.content
        mem = await interaction.guild.fetch_member(msg)
        await interaction.followup.send(
            embed=discord.Embed(
                description=f"<:tick:966707201064464395> Declined {mem.mention} as a staff.\n",
                color=discord.Color.green()
            )
        )


class StaffBtn(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)


    @discord.ui.button(label="Fill up.", style=discord.ButtonStyle.blurple, custom_id="StaffBtn", emoji="<a:badges:942447265744842762>")
    async def fill(self, button, interaction):
        quest = [
            [
                "What is your discord id?",
                "How old are you?",
                "How many servers are you moderating?",
                "Why you wanna moderate this server?",
                "What is your timezone?",
                "How long can you modrate in 1 day?",
                "Do you have any previous expreince moderating any server?,\nIf yes describe your expreince",
                "What is 2+2?"
            ],
            [
                "What will you do when 7 people joins the server within 30 seconds?",
                "What will you do when chat is very fast?",
                "What if someone is doing client modification?",
                "You suspect a member changing status very fast, whats happening there? What could be your action?",
                "How will you prevent a raid?",
                "Someone is spamming in the server, describe your action"
            ],
            [
                "What level are you in the server?",
                "Why should we choose you not anyone else?",
                "Your Speciality",
                "Describe yourself in 3 words.",
                "Descrie server in 3 words."
            ]
        ]
        ans = []

        await interaction.response.send_message(
            "Starting Staff Form Submission in dms.",
            ephemeral=True
        )

        try:
            await interaction.user.send(
                "Fetching Questions...",
            delete_after=2.0
        )
            sc = 1
            for sets in quest:
                qc = 1
                for q in sets:
                    em = discord.Embed(
                        title="Staff Form",
                        description=f"Set: {sc}",
                        color=discord.Color.random()
                    ).add_field(
                        name=f"<a:listening:942447554275201077> Question {qc}",
                        value=f"{q}",
                        inline=False
                    )
                    await interaction.user.send(
                        content=None,
                        embed=em
                    )
                    def check(msgg):
                        return isinstance(
                            msgg.channel,
                            discord.channel.DMChannel
                        ) and msgg.author.id == interaction.user.id

                    try:
                        msgg = await self.bot.wait_for(
                            'message',
                            check=check,
                            timeout=120.0
                        )
                    except TimeoutError:
                        await interaction.user.send("Timeout!")
                    else:
                        ans.append(
                            msgg.content
                        )
                        qc += 1
                sc += 1

            ch = self.bot.get_channel(FORMC)
            emb = discord.Embed(
                title="New Staff Submission!",
                description=f"React to accept or decline {interaction.user.mention} as a staff.",
                color=discord.Color.blurple(),
                timestamp=datetime.utcnow()
            ).set_author(name=f"{interaction.user.name}#{interaction.user.discriminator}",
                         icon_url=interaction.user.display_avatar
            ).set_thumbnail(
                url=interaction.user.display_avatar)

            cc = 0
            for sets in quest:
                qc = 1
                for q in sets:
                    emb.add_field(
                        name=f"#{qc}: {q}",
                        value=f"{ans[cc]}",
                        inline=False)
                    cc += 1
                    qc += 1

            await ch.send(
                f"{interaction.user.id}",
                embed=emb,
                view=SelectBtn(self.bot)
            )
            await interaction.user.send(
                "**Form Submitted!, Thanks you.**\n```If you get accepted we will send you a dm, else we will not reply!```"
            )

        except discord.Forbidden:
            await interaction.followup.send(
                "Your dms are off!",
                ephemeral=True
            )


class Form(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.staff_btn = False

    @commands.Cog.listener()
    async def on_ready(self):
        if self.staff_btn == False:
            self.bot.add_view(StaffBtn(bot=self.bot))
            self.bot.add_view(SelectBtn(self.bot))
            self.staff_btn = True

    @commands.command()
    @commands.is_owner()
    async def staff(self, ctx):
        await ctx.message.delete()
        em = discord.Embed(
            description="<a:badges:942447265744842762> Staff Apply",
            color=discord.Color.yellow()
        ).set_author(name="Ayu Itz", icon_url="https://images-ext-1.discordapp.net/external/9-gIQFvpi4nHHL_us7r_F5U0Qlqa7ik_H2f7qX6HV_U/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/823074724976001064/53d8a175e6f8a7bf97440aeabd0e8764.png?width=230&height=230"
                     ).add_field(
            name="Requirements",
            value="> <a:discordspin:942445611473596459> You must follow discord ToS and Privacy Policy\n> <a:discordspin:942445611473596459> You must have had been a moderator in any other server(we ask for proof)\n> <a:discordspin:942445611473596459> You must answer all questions\n> <a:discordspin:942445611473596459> You must be active at least 2-3hrs a day\n> <a:discordspin:942445611473596459> You must know English\n"
        ).add_field(
            name="** **",
            value="***__Note: you must meet all requirements if you want to be in staff__***,\nClick the Button Below to Apply"
        )

        await ctx.send(embed=em, view=StaffBtn(self.bot))


def setup(bot):
    bot.add_cog(Form(bot))
    print("Cog Loaded: Forms")
