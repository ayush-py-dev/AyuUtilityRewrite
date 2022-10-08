from time import time
import discord
from discord.ext import commands, tasks
import aiosqlite
from PIL import Image, ImageChops, ImageDraw, ImageFont
from io import BytesIO
from config import *
import DiscordUtils
from datetime import datetime, timedelta
import humanize

def circle(pfp,size = (950,950)):
    
    pfp = pfp.resize(size).convert("RGBA")
    
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp

class Welcome(commands.Cog):
    """
    A COG TO SEND MESSAGE WHEN A USER JOINS THE SERVER
    """
    def __init__(self, bot):
        self.bot = bot
        self.tracker = DiscordUtils.InviteTracker(bot)
        
    
    @commands.Cog.listener()
    async def on_member_join(self, member:discord.Member):
        """
        SEND A MESSAGE TO THE CHANNEL
        """
        ch = member.guild.get_channel(WEL_CH)
        log = member.guild.get_channel(LOGS)
        if member.bot:
            umb=member.guild.get_role(USERMADEBOTSROLES)
            await ch.send(f"> A {member.mention} summoned!")
            await member.add_roles(umb)
            emb=discord.Embed(
                title="Bot Joined!",
                description=f"It has been given the `{umb.name}` role!",
                color=discord.Color.dark_theme()
            ).set_thumbnail(
                url=member.default_avatar
            )
            return await log.send(embed=emb)
        bg=Image.open("asset/imgs/bg.png")
        av = member.display_avatar
        data = BytesIO(await av.read())
        pfp = Image.open(data)
        pfp=circle(pfp)


        title_font = ImageFont.truetype("asset/fonts/font.ttf", 250)
        defs = ImageFont.truetype("asset/fonts/font.ttf", 175)
        name_font = ImageFont.truetype("asset/fonts/font.ttf", 200)

        title=f"Welcome to the Server!"
        name=f"{member.name}"
        ids=f"> ID: {member.id}"
        inviter = await self.tracker.fetch_inviter(member)
        db=await aiosqlite.connect("Database/invites.db")
        cur=await db.execute("SELECT invcot FROM inv WHERE memid=?",(inviter.id,))
        
        if not inviter:
            inviter = "Ghost Probably"
            invites="INFINITE!!!"
        else:
            count=await cur.fetchone()
            if not count:
                await db.execute("INSERT INTO inv VALUES(?,?)",(inviter.id,1))
                await db.commit()
                count=1
            else:
                await db.execute("UPDATE inv SET invcot=? WHERE memid=?",(count[0]+1,inviter.id))
                await db.commit()
                count=count[0]+1
            inviter=f"> Inviter: {str(inviter)}"
            invites=f"> Invites: {count}"
        
        acc_created=f"> {humanize.naturaldelta(timedelta(seconds=int(time()-member.created_at.timestamp())))} old"


        draw=ImageDraw.Draw(bg)
        draw.text((600,10),text=title,font=title_font,fill="#ffffff")
        draw.text((1288,470),text=name,font=name_font,fill="#ffffff")
        draw.text((1348,844),text=ids,font=defs,fill="#ffffff")
        draw.text((1348,1044),text=inviter,font=defs,fill="#ffffff")
        draw.text((1348,1244),text=invites,font=defs,fill="#ffffff")
        draw.text((1348,1444),text=acc_created,font=defs,fill="#ffffff")

        bg.paste(pfp,(180,450),pfp)

        bg.save("asset/imgs/wel.png")
        await db.close()

        await ch.send(content=f"{member.mention}", file=discord.File("asset/imgs/wel.png"))

        

def setup(bot):
    bot.add_cog(Welcome(bot))
    print("Cog Loaded: Welcome")