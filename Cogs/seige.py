import discord
from discord.ext import commands
import asyncio
from siegeapi import Auth

from Utils.Json import *
from Utils.Crypto import *
from Utils.ManageUsers import *
from Utils.WebCrawling import *


class Seige(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Users = Users()
        self.R6Tracker = R6Tracker()
        
        self.YS = (7, 3) # 최신 시즌 Y7S4에 에러가 생겨 기본값은 이전 시즌인 Y7S3로 설정
        
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        
    
    @commands.command(aliases=["map", "맵"], description="Display top win rate maps")
    @commands.cooldown(rate=1, per=5)
    async def map_command(self, ctx, name, mode="a", count=5):
        async with ctx.typing():
            self.Users.load()
            if name.lower() not in map(lambda x: x.lower(), self.Users.df["name"].values):
                await ctx.send(f"유저 이름 `{name}`은 등록되지 않았습니다. 명령어 `login`을 통해 등록")
            else:
                email = self.Users.df.loc[self.Users.df["name"].str.lower() == name.lower()]["email"].values[0]
                password = decrypt(self.Users.df.loc[self.Users.df["name"].str.lower() == name.lower()]["password"].values[0])
                auth = Auth(email, password)
                player = await auth.get_player(name=name)
                
                await player.load_maps()
                date = player.maps.get_timespan_dates()["end_date"]
                if mode.lower() in ["a","all"]:
                    maps = player.maps.all.all
                    mode = "All"
                elif mode.lower() in ["r","rank"]:
                    maps = player.maps.ranked.all
                    mode = "Rank"
                elif mode.lower() in ["c","casual"]:
                    maps = player.maps.casual.all
                    mode = "Casual"
                elif mode.lower() in ["u","unrank"]:
                    maps = player.maps.unranked.all
                    mode = "Unrank"
                elif mode.lower() in ["n","newcomer"]:
                    maps = player.maps.newcomer.all
                    mode = "Newcomer"
                else:
                    maps = player.maps.all.all
                    mode = "All"
                    
                count = int(count) if len(maps) >= int(count) else 5
                map_embed = discord.Embed(
                    title=f"Top {count} Maps by win rate ({mode})",
                    description=f"~{date[0:4]}.{date[4:6]}.{date[6:8]}",
                    colour=0x3498db,
                    timestamp=ctx.message.created_at
                )
                map_embed.set_author(
                    name = player.name, 
                    url=self.R6Tracker.get_profile_url(id=player.id), 
                    icon_url=player.profile_pic_url
                )
                i = 0
                maps.sort(key=lambda m: m.matches_won/m.matches_played if m.matches_played != 0 else 0, reverse=True)
                for map_ in maps:
                    if i >= count: break
                    i += 1
                    map_embed.add_field(
                        name=f"Name: `{map_.map_name}`",
                        value=f"Win rate: `{map_.matches_won/map_.matches_played*100:.1f}%`\n"
                                f"Play mathces: `{map_.matches_played}`",
                        inline=False
                    )
                await ctx.send(embed=map_embed)
                
                await auth.close()
                
                
    @commands.command(aliases=["rank", "랭크"], description="")
    @commands.cooldown(rate=1, per=5)
    async def rank_command(self, ctx, name, y=0, s=0):
        async with ctx.typing():
            self.Users.load()
            if name.lower() not in map(lambda x: x.lower(), self.Users.df["name"].values):
                await ctx.send(f"유저 이름 `{name}`은 등록되지 않았습니다. 명령어 `login`을 통해 등록")
            else:
                email = self.Users.df.loc[self.Users.df["name"].str.lower() == name.lower()]["email"].values[0]
                password = decrypt(self.Users.df.loc[self.Users.df["name"].str.lower() == name.lower()]["password"].values[0])
                auth = Auth(email, password)
                player = await auth.get_player(name=name)
                
                if not (0 < y <= self.YS[0] and 0 < s <= self.YS[1]):
                    y, s = self.YS
                season = 4 * (y - 1) + s
                rank = await player.load_ranked(season=season)
                
                rank_embed = discord.Embed(
                    title=f"Y{y}S{s} Rank Stat",
                    colour=0x3498db,
                    timestamp=ctx.message.created_at
                )
                rank_embed.set_author(
                    name = player.name, 
                    url=self.R6Tracker.get_profile_url(id=player.id), 
                    icon_url=player.profile_pic_url
                )
                
                stat_lis = [
                    ["Max mmr", rank.max_mmr],
                    ["Max tier", rank.max_rank],
                    ["Last mmr", rank.mmr],
                    ["Kills", rank.kills],
                    ["Deaths", rank.deaths],
                    ["K/D", f"{rank.kills/rank.deaths:.2f}"],
                    ["Wins", rank.wins],
                    ["Losses", rank.losses],
                    ["Win rate", f"{rank.wins/(rank.wins+rank.losses)*100:.1f}"]
                ]
                for stat in stat_lis:
                    rank_embed.add_field(
                        name=stat[0],
                        value=stat[1],
                        inline=True
                    )
                await ctx.send(embed=rank_embed)
                
                await auth.close()


    @commands.command(aliases=["operator", "오퍼"], description="")
    @commands.cooldown(rate=1, per=5)
    async def operator_command(self, ctx, name, mode="a", count=5, operator_type="all"):
        async with ctx.typing():
            self.Users.load()
            if name.lower() not in map(lambda x: x.lower(), self.Users.df["name"].values):
                await ctx.send(f"유저 이름 `{name}`은 등록되지 않았습니다. 명령어 `login`을 통해 등록")
            else:
                email = self.Users.df.loc[self.Users.df["name"].str.lower() == name.lower()]["email"].values[0]
                password = decrypt(self.Users.df.loc[self.Users.df["name"].str.lower() == name.lower()]["password"].values[0])
                auth = Auth(email, password)
                player = await auth.get_player(name=name)
                
                await player.load_operators()
                date = player.operators.get_timespan_dates()["end_date"]
                if mode.lower() in ["a","all"]:
                    operators = player.operators.all
                    mode = "All"
                elif mode.lower() in ["r","rank"]:
                    operators = player.operators.ranked
                    mode = "Rank"
                elif mode.lower() in ["c","casual"]:
                    operators = player.operators.casual
                    mode = "Casual"
                elif mode.lower() in ["u","unrank"]:
                    operators = player.operators.unranked
                    mode = "Unrank"
                elif mode.lower() in ["n","newcomer"]:
                    operators = player.operators.newcomer
                    mode = "Newcomer"
                else:
                    operators = player.operators.all
                    mode = "All"
                    
                if operator_type.lower() == "all":
                    operators = operators.attacker + operators.defender
                elif operator_type.lower() in ["a", "attacker"]:
                    operators = operators.attacker
                elif operator_type.lower() in ["d", "defender"]:
                    operators = operators.defender
                    
                count = int(count) if len(operators) >= int(count) else 5
                    
                operator_embed = discord.Embed(
                    title=f"Top {count} Operator by k/d ({mode})",
                    description=f"~{date[0:4]}.{date[4:6]}.{date[6:8]}",
                    colour=0x3498db,
                    timestamp=ctx.message.created_at
                )
                operator_embed.set_author(
                    name = player.name, 
                    url=self.R6Tracker.get_profile_url(id=player.id), 
                    icon_url=player.profile_pic_url
                )
                i = 0
                operators.sort(key=lambda o: o.kills/o.death if o.death != 0 else 0, reverse=True)
                for operator_ in operators:
                    if i >= count: break
                    i += 1
                    operator_embed.add_field(
                        name=f"Name: `{operator_.name}`",
                        value=f"K/D: `{operator_.kills/operator_.death:.2f}`\n"
                            f"Win rate: `{operator_.matches_won/operator_.matches_played*100:.1f}%`\n"
                            f"Play mathces: `{operator_.matches_played}`",
                        inline=False
                    )
                await ctx.send(embed=operator_embed)
                
                await auth.close()
                

async def setup(bot):
    await bot.add_cog(Seige(bot))