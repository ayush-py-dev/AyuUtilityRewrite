"""
I would suggest not to touch anything as this cog is hardcoded.
Even I don't understand some parts now XD
If you have lots of free time (which I don't) you can always make it better
    and open a pull request :)
I would be very happy to merge
"""


import discord
from discord.ext import commands, tasks
import aiosqlite
from datetime import datetime
from random import randint, choice
from config import *

dbu = ""
dbm = ""

_id = {
    "ich": "🍒 iCherry",
    "wsi": "🌿 William Inc.",
    "soc": "🦾 Socialize",
    "gzi": "🎮 Gamezonic",
    "fsp": "🥾 Footworks Inc."
}

# async def create_table():
#     global dbm
#     await dbm.execute("""
#         CREATE TABLE IF NOT EXISTS bank(
#             memid TEXT,
#             coins INTEGER,
#             ich INTEGER,
#             wsi INTEGER,
#             soc INTEGER,
#             gzi INTEGER,
#             fsp INTEGER
#         )
#     """)
#     await dbm.commit()
#     print("table created")


class SearchButton(discord.ui.Button):
    def __init__(self, label: discord.Button.label, ctx: commands.Context):
        super().__init__(label=label, style=discord.ButtonStyle.blurple)
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        if not interaction.user.id == self.ctx.author.id:
            return await interaction.response.send_message("You can't search other people's accounts!", ephemeral=True)
        for i in self.view.children:
            i.disabled = True
        await self.view.msg.edit(view=self.view)
        global dbm
        cur = await dbm.execute("SELECT coins FROM bank WHERE memid=?", (interaction.user.id,))
        res = await cur.fetchone()
        if not res:
            em = discord.Embed(
                description="Start your account in the bank fool -_- where will u keep the money? in you a\*\*hole?\nDo `start-bank`", color=0xff9c9c)
            return await interaction.response.send_message(embed=em, delete_after=5)
        if choice([True, False]):
            amount = randint(15, 50)
            new_amount = res[0]+amount
            await dbm.execute("UPDATE bank SET coins=? WHERE memid=?", (new_amount, interaction.user.id))
            await dbm.commit()
            await interaction.response.send_message(embed=discord.Embed(description=f"You searched `{self.label}` and found {amount} <a:eco_coin:982662549952663562> coins which raised your balance to {new_amount} <a:eco_coin:982662549952663562> coins."))
        else:
            await interaction.response.send_message(embed=discord.Embed(description=f"You searched `{self.label}` but found nothing."))


class BegButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Beg", style=discord.ButtonStyle.blurple, custom_id="beggers")
    async def beg(self, button: discord.Button, interaction: discord.Interaction):
        luck = choice([True, False])
        amount = randint(1, 7)
        if not luck:
            em = discord.Embed(
                description="No one donated to you fella :( try your luck after sometime...", color=0xff9c9c)
            return await interaction.response.send_message(embed=em, delete_after=5, ephemeral=True)
        global dbm
        cur = await dbm.execute("SELECT coins FROM bank WHERE memid=?", (interaction.user.id,))
        res = await cur.fetchone()
        if not res:
            em = discord.Embed(
                description="Start your account in the bank fool -_- where will u keep the money? in you a\*\*hole?\nDo `start-bank`", color=0xff9c9c)
            return await interaction.response.send_message(embed=em, delete_after=5, ephemeral=True)
        new_amount = res[0]+amount
        await dbm.execute("UPDATE bank SET coins=? WHERE memid=?", (new_amount, interaction.user.id))
        await dbm.commit()
        await interaction.response.send_message(embed=discord.Embed(description=f"Someone donated you {amount} <a:eco_coin:982662549952663562> coins... You have {new_amount} <a:eco_coin:982662549952663562> coins in your bank now. Feeling Rich?", color=0xd6ff00), ephemeral=True)


class OfferView(discord.ui.View):
    def __init__(self, bot: commands.Bot, ctx: commands.Context, member: discord.Member, offer: int, ids: str, no: int):
        super().__init__(timeout=60)
        self.bot = bot
        self.ctx = ctx
        self.member = member
        self.offer = offer
        self.ids = ids
        self.no = no

    @discord.ui.button(label="Accept", custom_id="acceptoffer", style=discord.ButtonStyle.green)
    async def accept(self, button: discord.Button, interaction: discord.Interaction):
        if not interaction.user.id == self.member.id:
            await interaction.response.send_message(f"You're not the buyer", ephemeral=True)
        else:
            global dbm
            cur = await dbm.execute(f"SELECT {self.ids} FROM bank WHERE memid=?", (self.ctx.author.id,))
            author_share = await cur.fetchone()
            cur = await dbm.execute(f"SELECT {self.ids} FROM bank WHERE memid=?", (self.member.id,))
            member_share = await cur.fetchone()
            cur = await dbm.execute(f"SELECT coins FROM bank WHERE memid=?", (self.ctx.author.id,))
            author_coins = await cur.fetchone()
            cur = await dbm.execute(f"SELECT coins FROM bank WHERE memid=?", (self.member.id,))
            member_coins = await cur.fetchone()
            # intense calculations here ;-;
            total = self.no * self.offer
            new_author_coins = author_coins[0] + total
            new_member_coins = member_coins[0] - total
            new_author_share = author_share[0] - self.no
            new_member_share = member_share[0] + self.no

            await dbm.execute(f"UPDATE bank SET {self.ids}=?, coins=? WHERE memid=?", (new_author_share, new_author_coins, self.ctx.author.id))
            await dbm.execute(f"UPDATE bank SET {self.ids}=?, coins=? WHERE memid=?", (new_member_share, new_member_coins, self.member.id))

            await dbm.commit()

            for i in self.children:
                i.disabled = True
            await interaction.message.edit(view=self)
            await interaction.response.send_message(embed=discord.Embed(description="Wow what a great deal signed!", color=0xd0ff85))

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def deny(self, button: discord.Button, interaction: discord.Interaction):
        if not interaction.user.id == self.member.id:
            return await interaction.response.send_message(f"You're not the buyer", ephemeral=True)
        for i in self.childern:
            i.disabled = True
        await interaction.message.edit(view=self)
        await interaction.response.send_message(embed=discord.Embed(description=f":x: Offer declined ._.", color=0xff9c9c))

    async def on_timeout(self):
        for i in self.children:
            i.disabled = True
        await self.msg.edit(view=self)


class Economy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.beg_btn = False

    @commands.Cog.listener()
    async def on_ready(self):
        if self.beg_btn == False:
            self.bot.add_view(BegButton())
            self.beg_btn = True
        global dbu
        global dbm
        dbu = await aiosqlite.connect("Database/Economy/mprice.db")
        dbm = await aiosqlite.connect("Database/Economy/users.db")
        await set_rate.start(self.bot)

    @commands.command()
    @commands.is_owner()
    async def showrate(self, ctx):
        msg = await ctx.send("This will be the msg for rates")
        print(msg.id)
        print(msg.channel.id)

    @commands.command()
    @commands.is_owner()
    async def setvalues(self, ctx):
        global dbu
        names = ["ich", "wsi", "soc", "gzi", "fsp"]
        vals = [1000, 1500, 500, 2000, 1300]
        s = 0
        for i in names:
            await dbu.execute("INSERT INTO market VALUES(?,?)", (i, vals[s]))
            s += 1
        await dbu.commit()
        await ctx.reply("added values")

    @commands.command(name="start-bank", aliases=["sb"])
    async def eco(self, ctx):
        global dbm
        cur = await dbm.execute("SELECT coins FROM bank WHERE memid=?", (ctx.author.id,))
        res = await cur.fetchone()
        if res:
            return await ctx.reply(embed=discord.Embed(description=f"You already have an account with {res[0]} <a:eco_coin:982662549952663562> coins in it."))
        await dbm.execute("INSERT INTO bank VALUES(?,?,?,?,?,?,?)", (ctx.author.id, 1000, 0, 0, 0, 0, 0))
        await dbm.commit()
        await ctx.reply("Bank account created!")

    @commands.command(name="balance", aliases=["bal", "inv", "inventory"])
    async def bank(self, ctx, member: discord.Member = None):
        """
        Shows user's inventory
        **Syntax:** +[balance|bal|inv|inventory] [user]
        """
        if not member:
            member = ctx.author
        global dbm
        cur = await dbm.execute("SELECT * FROM bank WHERE memid=?", (member.id,))
        data = await cur.fetchone()
        if not data:
            em = discord.Embed(
                description="There is no bank associated with that user. Do `+start-bank` to create one", color=0xff9c9c)
            await ctx.send(embed=em)
        else:
            global dbu
            names = ["ich", "wsi", "soc", "gzi", "fsp"]
            cp = []
            net_worth = data[1]
            for i in names:
                cur = await dbu.execute("SELECT vale FROM market WHERE cname=?", (i,))
                res = await cur.fetchone()
                cp.append(res[0])
            for c, i in enumerate(cp):
                net_worth += i*data[c+2]
            em = discord.Embed(
                description="**{}'s** inventory:".format(member.name), color=0x00ff00)
            em.add_field(
                name="<a:eco_coin:982662549952663562> Coins", value=data[1])
            em.add_field(name="🍒 iCherry", value=data[2])
            em.add_field(name="🌿 William Inc.", value=data[3])
            em.add_field(name="🦾 Socialize", value=data[4])
            em.add_field(name="🎮 Gamezonic", value=data[5])
            em.add_field(name="🥾 Footworks Inc.", value=data[6])
            em.add_field(
                name="** **", value=f"<:inventory:982676105179836437>  Net worth: <a:eco_coin:982662549952663562> {net_worth}", inline=False)
            await ctx.send(embed=em)

    @commands.command(name="shop", aliases=["sh"])
    async def shop(self, ctx):
        """
        Shows the shop
        **Syntax:** +[shop|sh]
        """

        global dbu
        cp = []
        names = ["ich", "wsi", "soc", "gzi", "fsp"]
        for i in names:
            cur = await dbu.execute("SELECT vale FROM market WHERE cname=?", (i,))
            res = await cur.fetchone()
            cp.append(res[0])
        em = discord.Embed(description="Buy using id:", color=0xab66ff)
        em.add_field(
            name="🍒 iCherry `id:ich`",
            value="<a:eco_coin:982662549952663562> {} coins".format(cp[0]),
            inline=False
        ).add_field(
            name="🌿 William Inc. `id:wsi`",
            value="<a:eco_coin:982662549952663562> {} coins".format(cp[1]),
            inline=False
        ).add_field(
            name="🦾 Socialize `id:soc`",
            value="<a:eco_coin:982662549952663562> {} coins".format(cp[2]),
            inline=False
        ).add_field(
            name="🎮 Gamezonic `id:gzi`",
            value="<a:eco_coin:982662549952663562> {} coins".format(cp[3]),
            inline=False
        ).add_field(
            name="🥾 Footworks Inc. `id:fsp`",
            value="<a:eco_coin:982662549952663562> {} coins".format(cp[4]),
            inline=False
        )
        em.set_footer(text="Use \"+buy <id> <no-of-shares>\" to buy share.")
        await ctx.reply(embed=em)

    @commands.command(name="buy", aliases=["b"])
    async def buy(self, ctx, ids: str, no: int):
        """
        Buys shares of a company
        **Syntax:** +[buy|b] <id> <no-of-shares>
        """
        if no < 1:
            return await ctx.reply("How can you buy shares in negative?", color=0xff9c9c)
        global dbm
        global dbu
        cur2 = await dbm.execute(f"SELECT coins FROM bank WHERE memid=?", (ctx.author.id,))
        cur = await dbu.execute(f"SELECT vale FROM market WHERE cname=?", (ids,))
        rate = await cur.fetchone()
        data = await cur2.fetchone()
        if not data:
            em = discord.Embed(
                description="There is no bank associated with you. Do `+start-bank` to create one", color=0xff9c9c)
            await ctx.reply(embed=em)
        elif not rate:
            return await ctx.reply(embed=discord.Embed(description=":x: There is no item with that tag in the shop", color=0xff9c9c))
        else:
            if rate[0]*no > data[0]:
                return await ctx.reply(embed=discord.Embed(description=":x: Not enough money to buy shares.", color=0xff9c9c))
            else:
                cur = await dbm.execute(f"SELECT {ids} FROM bank WHERE memid=?", (ctx.author.id,))
                res = await cur.fetchone()
                new = res[0]+no
                await dbm.execute(f"UPDATE bank SET {ids}=? WHERE memid=?", (new, ctx.author.id))
                money = data[0]-rate[0]*no
                await dbm.execute("UPDATE bank SET coins=? WHERE memid=?", (money, ctx.author.id))
                await dbm.commit()
                item = _id[f"{ids}"]
                await ctx.reply(embed=discord.Embed(description=f"Bought `{no}` shares of `{item}` at `{rate[0]}` per share, you are now left with `{money}` coins!", color=0xd0ff85))

    @commands.command(name="sell", aliases=["s"])
    async def sell(self, ctx, ids: str, no: int):
        """
        Sells shares of a company
        **Syntax:** +[sell|s] <id> <no-of-shares>
        """
        if no < 1:
            return await ctx.reply(embed=discord.Embed("How can you sell shares in negative?"), color=0xff9c9c)
        global dbm
        global dbu
        try:
            cur2 = await dbm.execute(f"SELECT {ids} FROM bank WHERE memid=?", (ctx.author.id,))
        except:
            return await ctx.reply(embed=discord.Embed(description=":x: There is no item with that tag in the bank", color=0xff9c9c))
        cur = await dbu.execute(f"SELECT vale FROM market WHERE cname=?", (ids,))
        rate = await cur.fetchone()
        data = await cur2.fetchone()
        if not data:
            em = discord.Embed(
                description="There is no bank associated with you. Do `+start-bank` to create one", color=0xff9c9c)
            await ctx.reply(embed=em)
        elif not rate:
            return await ctx.reply(embed=discord.Embed(description=":x: There is no item with that tag in the shop", color=0xff9c9c))
        else:
            if no > data[0]:
                return await ctx.reply(embed=discord.Embed(description=":x: You don't have that many shares.", color=0xff9c9c))
            else:
                cur = await dbm.execute(f"SELECT coins FROM bank WHERE memid=?", (ctx.author.id,))
                res = await cur.fetchone()
                new = res[0]+rate[0]*no
                await dbm.execute(f"UPDATE bank SET coins=? WHERE memid=?", (new, ctx.author.id))
                money = data[0]-no
                await dbm.execute(f"UPDATE bank SET {ids}=? WHERE memid=?", (money, ctx.author.id))
                await dbm.commit()
                item = _id[f"{ids}"]
                await ctx.reply(embed=discord.Embed(description=f"Sold `{no}` shares of `{item}` at `{rate[0]}` per share, you are now left with `{money}` shares!", color=0xd0ff85))

    @commands.command(name="offer", aliases=["off"])
    @commands.cooldown(2, 70, commands.BucketType.user)
    async def offer(self, ctx, member: discord.Member, ids: str, no: int, rate: int):
        """
        Offers shares of a company to a user
        **Syntax:** +[offer|off] <member> <id> <no-of-shares> <rate>
        """
        global dbm
        try:
            await dbm.execute(f"SELECT {ids} FROM bank WHERE memid=?", (ctx.author.id,))
        except:
            return await ctx.reply(embed=discord.Embed(description=":x: There is no item with that tag in the bank", color=0xff9c9c))
        cur = await dbm.execute(f"SELECT {ids} FROM bank WHERE memid=?", (ctx.author.id,))
        no_of_shares = await cur.fetchone()
        cur = await dbm.execute(f"SELECT {ids} FROM bank WHERE memid=?", (member.id,))
        member_shares = await cur.fetchone()
        cur = await dbm.execute("SELECT coins FROM bank WHERE memid=?", (member.id,))
        member_money = await cur.fetchone()
        if not no_of_shares:
            return await ctx.reply(embed=discord.Embed(description=":x: You don't have account associated with the bank. Do `start-bank` to create one.", color=0xff9c9c))
        if not member_shares:
            return await ctx.reply(embed=discord.Embed(description=":x: The user don't have account associated with the bank.", color=0xff9c9c))
        if no_of_shares[0] < no:
            return await ctx.reply(embed=discord.Embed(description=f":x: You don't have enough shares to sell.", color=0xff9c9c))
        if member_money[0] < no*rate:
            return await ctx.reply(embed=discord.Embed(description=f":x: User don't have enough money to buy shares.", color=0xff9c9c))
        item = _id[f"{ids}"]
        total = no*rate
        view = OfferView(bot=self.bot, ctx=ctx, member=member,
                         offer=rate, ids=ids, no=no)
        view.msg = await ctx.reply(content=f"**Offer between {ctx.author.mention} and {member.mention}**", embed=discord.Embed(description=f"{member.mention} have `60 seconds` to confirm this prompt!", color=0xd0ff85).add_field(name="What's the offer?", value=f"{ctx.author.mention} is trying to sold you **{no}** shares of **{item}** at the rate of **{rate}** per shares, which will evaluate to **<a:eco_coin:982662549952663562> {total}**", inline=False), view=view)

    @commands.command(name="show-beg-button")
    @commands.is_owner()
    async def show_beg(self, ctx: commands.Context):
        em = discord.Embed(
            description=":eyes: Look at this begger...\nTry your luck to beg again...",
            color=0xb672ff
        )
        await ctx.send(embed=em, view=BegButton())

    @commands.command(name="search", aliases=["look"])
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def search(self, ctx: commands.Context):
        """
        Search somewhere
        **Syntax:** +[look|search]
        """
        places = ["Ship", "Butt", "Sewer", "Dog house", "Ayu's basement", "Police van", "Discord", "Pocket",
                  "Your mom", "Kitchen", "Bedroom", "Knowhere", "Shell", "Pillow", "Car", "Shit", "Everywhere"]
        select = []
        view = discord.ui.View(timeout=10)
        for i in range(3):
            place = choice(places)
            if not place in select:
                select.append(place)
                view.add_item(SearchButton(label=place, ctx=ctx))

        em = discord.Embed(
            description="Select a place to search:", color=0x718eff)
        view.msg = await ctx.reply(embed=em, view=view)

    @commands.command(name="bet", aliases=["slot"])
    @commands.cooldown(3, 60, commands.BucketType.user)
    async def bet(self, ctx, coin: int = 150):
        """
        Gamble the amount
        **Syntax:** +[bet|slot] [150`>`coins`>`10000]
        """
        global dbm
        cur = await dbm.execute("SELECT coins FROM bank WHERE memid=?", (ctx.author.id,))
        res = await cur.fetchone()
        if not res:
            return await ctx.reply(embed=discord.Embed(description="❌ You don't have account associated with the bank. Do `start-bank` to create one.", color=0xff9c9c))
        if coin < 150 or coin > 10000:
            return await ctx.reply(embed=discord.Embed(description="Betting amount should be between 150-10000"))
        if res[0] < coin:
            return await ctx.reply(embed=discord.Embed(description="❌ Not enough money to bet.", color=0xff9c9c))

        emojis = ["🍌", "🍑", "🍆", "🍇"]
        luck = []
        for _ in range(3):
            luck.append(choice(emojis))
        emo = ""
        for i in luck:
            emo = f"{emo}{i}"

        if luck[0] == luck[1] and luck[1] == luck[2] and luck[0] == luck[2]:
            title = "JACKPOT!!!"
            wins = coin*9
            message = f"You won a jackpot of <a:eco_coin:982662549952663562> {coin*10} coins!!!"
            color = 0x29ff00
        # win
        elif luck[0] == luck[1] or luck[1] == luck[2]:
            title = "WIN!"
            wins = coin
            message = f"You won the bet and doubled money to <a:eco_coin:982662549952663562> {coin*2} coins!"
            color = 0xfaff00
        # lose
        else:
            title = "LOST"
            wins = -coin
            message = f"You lost <a:eco_coin:982662549952663562> {coin} coins"
            color = 0xff1d00

        await dbm.execute("UPDATE bank SET coins=coins+? WHERE memid=?", (wins, ctx.author.id))
        await dbm.commit()

        em = discord.Embed(
            title=title,
            description=f"<a:slots:983375452532002857> Slot:\n{emo}\n{message}",
            color=color
        )

        await ctx.reply(embed=em)

    @commands.command(name="leaderboard", aliases=["lb", "top", "rich", "leaderboards"])
    @commands.cooldown(1, 60, commands.BucketType.member)
    async def leader(self, ctx: commands.Context):
        """
        Show the leaderboard
        **Syntax:** +[leaderboard|lb|top|rich|leaderboards]
        """
        global dbm
        cur = await dbm.execute("SELECT * FROM bank ORDER BY coins DESC")
        res = await cur.fetchmany(9)
        embed = discord.Embed(
            description="Richest user of Economy.", color=discord.Color.random())
        for i in res:
            member = await self.bot.fetch_user(i[0])
            embed.add_field(
                name=f"{str(member)}",
                value=f" {i[1]} <a:eco_coin:982662549952663562> coins",
                inline=False
            )
        await ctx.reply(embed=embed)

    @commands.command(name="give", aliases=["give-money", "give-money-to", "donate"])
    @commands.cooldown(1, 20, commands.BucketType.member)
    async def give_money(self, ctx: commands.Context, member: discord.Member, amount: int):
        """
        Donate money to a member
        **Syntax:** +[give|give-money|give-money-to|donate] <member> <amount>
        """
        global dbm
        cur = await dbm.execute("SELECT coins FROM bank WHERE memid=?", (ctx.author.id,))
        res = await cur.fetchone()
        if not res:
            return await ctx.reply(embed=discord.Embed(description="❌ You don't have account associated with the bank. Do `start-bank` to create one.", color=0xff9c9c))
        if res[0] < amount:
            return await ctx.reply(embed=discord.Embed(description="❌ Not enough money to donate.", color=0xff9c9c))
        try:
            cur = await dbm.execute("SELECT coins FROM bank WHERE memid=?", (member.id,))
            res = await cur.fetchone()
            if not res:
                return await ctx.reply(embed=discord.Embed(description="❌ The member doesn't have account associated with the bank. Do `start-bank` to create one.", color=0xff9c9c))
        except:
            return await ctx.reply(embed=discord.Embed(description="❌ The member doesn't have account associated with the bank. Do `start-bank` to create one.", color=0xff9c9c))
        await dbm.execute("UPDATE bank SET coins=coins-? WHERE memid=?", (amount, ctx.author.id))
        await dbm.execute("UPDATE bank SET coins=coins+? WHERE memid=?", (amount, member.id))
        await dbm.commit()
        await ctx.reply(embed=discord.Embed(description=f"💰 Successfully donated <a:eco_coin:982662549952663562> {amount} coins to {member.mention}", color=0x00ff00))


@tasks.loop(minutes=5)
async def set_rate(bot: discord.Bot):
    global dbu

    ch = bot.get_channel(ECRCH)
    msg = await ch.fetch_message(ECRMG)
    names = ["ich", "wsi", "soc", "gzi", "fsp"]
    cp = []
    np = []
    for i in names:
        cur = await dbu.execute("SELECT vale FROM market WHERE cname=?", (i,))
        res = await cur.fetchone()
        cp.append(res[0])
    day = datetime.utcnow().strftime("%A")
    strs = f"Day: {day}, Note: Markets are closed on Sunday"
    if day == "Sunday":
        strs = F"It's {day}, The markets are closed today "
        np = cp
    else:
        for i in cp:
            if choice([True, False]):
                i += randint(3, 9)
                np.append(i)
            else:
                i -= randint(3, 9)
                np.append(i)
        for c, val in enumerate(names):
            await dbu.execute("UPDATE market SET vale=? WHERE cname=?", (np[c], val))
    await dbu.commit()
    em = discord.Embed(
        title="Company Evaluation:",
        color=discord.Color.random()
    ).add_field(
        name="🍒 iCherry",
        value=f"{np[0]}"
    ).add_field(
        name="🌿 William Inc.",
        value=f"{np[1]}"
    ).add_field(
        name="🦾 Socialize",
        value=f"{np[2]}"
    ).add_field(
        name="🎮 Gamezonic",
        value=f"{np[3]}"
    ).add_field(
        name="🥾 Footworks Inc.",
        value=f"{np[4]}"
    ).set_footer(
        text=strs
    )
    await msg.edit(content=None, embed=em)


def setup(bot):
    bot.add_cog(Economy(bot))
    print("Cog loaded: Economy")
