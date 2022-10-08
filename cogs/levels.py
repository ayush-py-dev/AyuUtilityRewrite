import discord, aiosqlite
from discord.ext import commands
from PIL import Image, ImageDraw, ImageChops, ImageFont
from config import *
import requests
from io import BytesIO
from easy_pil import Editor,Canvas

def circle(pfp,size = (110,110)):
    
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")
    
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp

def make_banner(av,bg,lvl,xp,req,text,color,color2):

    percent=round(xp/req*100)

    if xp>=1000:
        xp=f"{round(xp/1000,1)}K"
    else:
        xp=round(xp)
    if req>=1000:
        req=f"{round(req/1000,1)}K"
    else:
        req=round(req)


    sub=f"Level: {lvl}   XP : {xp}/{req}"

    font1  = ImageFont.truetype("asset/fonts/font.otf",44)
    font2  = ImageFont.truetype("asset/fonts/font.otf",38)
    pfp    = Image.open(av)
    # bg     = Image.open(bg)


    pfp=circle(pfp)
    bg=bg.crop((0,0,800,200))
    bg.paste(pfp,(15,15),pfp)
    draw=ImageDraw.Draw(bg)
    draw.text((148,20),text,color2,font1)
    draw.text((148,75),sub,color2,font2)
    bg=Editor(bg)
    bg.rectangle((10,150),width=630,height=34,fill=color2,radius=20)
    bg.bar((10,150),max_width=630,height=34,fill=color,radius=20,percentage=percent)
    bg.rectangle((145,75),width=256,height=3,fill=color)
    border= Canvas((400,400),color=color)
    border= Editor(border)
    border.rotate(45.0,expand=True)
    bg.paste(border,(531,-290))

    return bg



class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(
        name="set-baner",
        guidl_ids=[GUILD_ID],
        description="""Create custom banner for levels! NO NSFW!"""
    )
    @commands.has_any_role(
        810419731575996416,
        1000072283282477158
    )
    async def set_banner(
        self,
        ctx: commands.Context,
        bg_img_url = None
        ,primary_color = None
        ,secondry_color = None
    ):
        await ctx.respond(
            "Updating your custom background!"
        )


        db=await aiosqlite.connect("Database/levels.db")
        cur=await db.execute("SELECT * FROM lvl WHERE memid=?",(ctx.author.id,))
        res=await cur.fetchone()

        bg_img_url = bg_img_url or res[4]
        primary_color = primary_color or res[5]
        secondry_color = secondry_color or res[6]

        try:
            Image.open(
                requests.get(
                    bg_img_url,
                    stream=True
                ).raw
            )
        except Exception as e:
            await ctx.respond(
                "That image cannot be used for some reason!"
            )
            print(e)
        def check_color(primary, secondry) -> bool:
            if primary.startswith("#") and secondry.startswith("#") and len(primary)==7 and len(secondry)==7:
                return True
        
        if check_color(primary = primary_color, secondry = secondry_color):
            await db.execute("""UPDATE lvl
                    SET imgurl = ?,
                        primcol = ?,
                        seccol = ?
                    WHERE memid = ?
                """,
                (
                    bg_img_url,
                    primary_color,
                    secondry_color,
                    ctx.author.id
                )
            )
            
            await db.commit()

            av = ctx.author.display_avatar
            data = BytesIO(await av.read())
            url=bg_img_url
            bg=Image.open(requests.get(url,stream=True).raw)

            bg=make_banner(data,bg,res[3],res[1],res[2],f"{ctx.author.name}#{ctx.author.discriminator}",primary_color,secondry_color)



            with BytesIO() as image_binary:
                        bg.save(image_binary, 'PNG')
                        image_binary.seek(0)
                        await ctx.respond("This is how your level message will look!",file=discord.File(fp=image_binary, filename=f'level.png'))
        else:
            await ctx.respond("Color code should be #hex123")
        await db.close()
        

    


    @commands.slash_command(guild_ids=[GUILD_ID],description="""Shows the level""")
    async def level(self,ctx,member:discord.Member=None):
        if not member:
            member=ctx.author
        if member.bot: return await ctx.respond(
            f"{member.mention} is a bot!",
            ephemeral=True
        )
        responsed = await ctx.respond(
            "Fetching level...",
        )
        db=await aiosqlite.connect("Database/levels.db")
        cur=await db.execute("SELECT * FROM lvl WHERE memid=?",(member.id,))
        res=await cur.fetchone()
        await db.close()
        av = member.display_avatar
        data = BytesIO(await av.read())
        url=str(res[4])
        # print(url)
        maintext=f"{member.name}#{member.discriminator}"
        bg=Image.open(requests.get(url,stream=True).raw)
        xp=res[1]
        req=res[2]
        lev=res[3]
        prim=res[5]
        sec=res[6]

        banner=make_banner(data,bg,lev,xp,req,maintext,prim,sec)

        with BytesIO() as image_binary:
            banner.save(image_binary, 'PNG')
            image_binary.seek(0)
            await responsed.edit_origianl_message(
                content = 
                f"**{member.mention}'s level:**",
                file=discord.File(
                    fp=image_binary,
                    filename=f'level.png'
                )
            )
        
    
    @commands.slash_command(guild_ids=[GUILD_ID],description="""Shows the leaderboard""")
    async def leaderboard(self,ctx):
        response = await ctx.respond(
            "Fetching leaderboard..."
        )
        db=await aiosqlite.connect("Database/levels.db")
        cur=await db.execute("SELECT * FROM lvl ORDER BY lev DESC")
        res=await cur.fetchall()
        embed=discord.Embed(
            title="Leaderboard",
            description="**Top 10**",
            color=0x00ff00
        )
        for i in range(10):
            try:
                embed.add_field(
                    name=f"#{i+1}. {self.bot.get_user(res[i][0]).name}#{self.bot.get_user(res[i][0]).discriminator}",
                    value=f"Level: {res[i][3]}",
                    inline=False
                )
            except:
                pass
        await response.edit_original_message(embed=embed)
        await db.close()

    @commands.Cog.listener()
    async def on_message(self,msg):
        if msg.author.bot:
            return
        try:
            if msg.guild.id==GUILD_ID:
                xp:float=0
                boost = 0.1
                bump_role = msg.guild.get_role(
                    1018184721647292516
                )
                if bump_role in msg.author.roles:
                    boost=0.2
                if msg.author.premium_since:
                    boost=0.4
                for i in msg.content:
                    xp+=boost
                db = await aiosqlite.connect("Database/levels.db")
                cur=await db.execute("SELECT * FROM lvl WHERE memid=?",(msg.author.id,))
                res=await cur.fetchone()
                if not res:
                    imgurl="https://wallpaperaccess.com/full/2200497.jpg"
                    pcol="#42caff"
                    scol="#ffffff"
                    await db.execute("INSERT INTO lvl VALUES(?,?,?,?,?,?,?)",(msg.author.id,xp,100,1,imgurl,pcol,scol))
                else:
                    oxp=res[1]
                    nxp=oxp+xp
                    await db.execute("UPDATE lvl SET xp=? WHERE memid=?",(nxp,msg.author.id))
                await db.commit()
                if nxp>=res[2]:
                    for role in msg.guild.roles:
                        if f"「 Level {res[3]+1} + 」" in role.name:
                            await msg.author.add_roles(role)
                            break
                    em=discord.Embed(
                        title=" ",
                        description=f"<:upvote:942683497204691014> GG! {msg.author.mention} You are now at level **{res[3]+1}**",
                        color=discord.Color.green()
                        )
                    xp=1.00
                    xpreq=res[2]+100
                    lvl=res[3]+1
                    await db.execute("""
                    UPDATE lvl
                    SET xp=?,
                        xpreq = ?,
                        lev = ?
                    WHERE memid=?
                    """,(xp,xpreq,lvl,msg.author.id))
                    await db.commit()
                    await msg.channel.send(embed=em)
                await db.close()
        except Exception as e: print(e)

            

def setup(bot):
    bot.add_cog(Levels(bot))
    print("Cog loaded: Levels")
