import discord
from discord.ext import commands
import asyncio
import re
from siegeapi import Auth

from Utils.Json import *
from Utils.Crypto import *
from Utils.ManageUsers import *
from Utils.WebCrawling import *


class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Users = Users()
        self.R6Tracker = R6Tracker()

        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
    
    
    @commands.command(aliases=["login", "로그인"], description="Search R6S user by name")
    @commands.cooldown(rate=1, per=5)
    async def login_command(self, ctx):
        async with ctx.author.typing():
            await ctx.author.send("이메일을 입력해주세요.")
            
            def check(m):
                return ctx.author.id == m.author.id and isinstance(m.channel, discord.DMChannel)
            
            try:
                email = await self.bot.wait_for("message", check=check, timeout=20)
            except asyncio.TimeoutError:
                await ctx.author.send("시간 초과")
            else:
                email = email.content
                regex = r"^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$"
                if not re.match(regex, email):
                    await ctx.author.send("잘못된 이메일 형식입니다.")
                else:
                    await ctx.author.send("비밀번호를 입력해주세요.")
                    try:
                        password = await self.bot.wait_for("message", check=check, timeout=20)
                    except asyncio.TimeoutError:
                        await ctx.author.send("시간 초과")
                    else:
                        password = password.content
                        encrypt_password = encrypt(password)
                        await ctx.author.send("닉네임을 입력해주세요.")
                        try:
                            name = await self.bot.wait_for("message", check=check, timeout=20)
                        except asyncio.TimeoutError:
                            await ctx.author.send("시간 초과")
                        else:
                            name = name.content
                            try:
                                auth = Auth(email, password)
                                player = await auth.get_player(name=name)
                            except:
                                await ctx.author.send("로그인 실패")
                            else:
                                await player.load_progress()
                                if player.level == 0:
                                    await ctx.author.send("로그인 실패")
                                else:
                                    await ctx.author.send("로그인 성공")
                                    user = {
                                        "email": email,
                                        "password": encrypt_password,
                                        "id": player.id,
                                        "name": player.name,
                                    }
                                    self.Users.load()
                                    self.Users.update(user)
                                    self.Users.save()
                            finally:
                                await auth.close()
                                

    @commands.command(aliases=["user", "유저"], description="Show favorite users")
    @commands.cooldown(rate=1, per=5)
    async def user_command(self, ctx, name):
        async with ctx.typing():
            self.Users.load()
            if name.lower() not in map(lambda x: x.lower(), self.Users.df["name"].values):
                await ctx.send(f"유저 이름 `{name}`은 등록되지 않았습니다. 명령어 `login`을 통해 등록")
            else:
                email = self.Users.df.loc[self.Users.df["name"].str.lower() == name.lower()]["email"].values[0]
                password = decrypt(self.Users.df.loc[self.Users.df["name"].str.lower() == name.lower()]["password"].values[0])
                auth = Auth(email, password)
                player = await auth.get_player(name=name)
                url = self.R6Tracker.get_url_by_id(player.id)
                user_embed = discord.Embed(
                    title="R6 Tracker URL",
                    url=url,
                    colour=0xe74c3c,
                    timestamp=ctx.message.created_at
                )
                name = player.name
                user_embed.set_author(
                    name=name, 
                    url=self.R6Tracker.get_profile_url(id=player.id), 
                    icon_url=player.profile_pic_url
                )
                await player.load_progress()
                user_embed.add_field(
                    name=f"Level",  
                    value=f"`{player.level}` lvl",
                    inline=True
                )
                await player.load_playtime()
                user_embed.add_field(
                    name=f"Play Time", 
                    value=f"`{player.total_time_played/3600:.1f}` hours",
                    inline=True
                )
                await ctx.send(embed=user_embed)

                await auth.close()
                            
                
    @commands.command(aliases=["search", "검색"], description="Search R6S user by name")
    @commands.cooldown(rate=1, per=5)
    async def search_command(self, ctx, name):
        async with ctx.typing():
            name = self.R6Tracker.get_proper_name(name)
            profile_url = self.R6Tracker.get_profile_url(name=name)
            if profile_url is not None:
                search_embed = discord.Embed(
                    title="R6 Tracker URL",
                    url=profile_url,
                    description=f"Successfully found `{name}` user",
                    colour=0xe67e22,
                    timestamp=ctx.message.created_at
                )
                search_embed.set_author(
                    name=name, 
                    url=profile_url, 
                    icon_url=self.R6Tracker.get_profile_icon_url(name=name)
                )
            else:
                search_embed = discord.Embed(
                    title=f"Failed to find `{name}` user",
                    colour=0xe67e22,
                    timestamp=ctx.message.created_at
                )
            await ctx.send(embed=search_embed)

async def setup(bot):
    await bot.add_cog(User(bot))