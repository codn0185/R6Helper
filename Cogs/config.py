import discord
from discord.ext import commands
import asyncio

from Utils.Json import *
from constants.prefix import prefix_list


class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.foldername = "Cogs"
        
        if not is_json("guilds"):
            write_json({}, "guilds")
        self.guilds = read_json("guilds")
        
        self.default_prefix = "!"
        

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded")
        
        
    @commands.command(aliases=["setting", "설정"], description="")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(rate=1, per=5)
    async def setting_command(self, ctx):
        async with ctx.typing():
            guild_id = str(ctx.guild.id)
            channel_id = str(ctx.channel.id)

            try:
                guilds = read_json("guilds")
            except:
                guilds = {}
            guilds[guild_id] = guilds.get(guild_id, {})
            guilds[guild_id]["prefix"] = self.default_prefix
            guilds[guild_id]["channel_id"] = channel_id
            write_json(guilds, "guilds")
            

    @commands.command(aliases=["reset", "초기화"], description="")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(rate=1, per=5)
    async def reset_command(self, ctx):
        async with ctx.typing():
            guild_id = str(ctx.guild.id)
            
            await ctx.send("정말 초기화 하실 건가요? (y/n)")
            
            def check(m):
                return ctx.author.id == m.author.id and ctx.channel.id == m.channel.id and m.content in ["y", "n"] 
            
            try:
                msg = await self.bot.wait_for("message", check=check, timeout=10)
            except asyncio.TimeoutError:
                await ctx.send("시간 초과")
            else:
                msg = msg.content
                if msg == "y":
                    await ctx.send("초기화 진행 중...")
                    guilds = read_json("guilds")
                    guilds[guild_id] = {}
                    write_json(guilds, "guilds")
                    await ctx.send("초기화 완료")
                else:
                    await ctx.send("초기화 중단")
                    
                
    @commands.command(aliases=["prefix", "접두사"], description="")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    async def prefix_command(self, ctx, *, pre="!"):
        guild_id = str(ctx.guild.id)
        async with ctx.typing():
            if pre in prefix_list:
                prefix = pre
                await ctx.send(f"명령어의 접두사가 `{pre}`로 설정되었습니다.")
            else:
                prefix = self.default_prefix
                await ctx.send(f"`{pre}`는 설정 불가능한 접두사입니다. 자동으로 접두사는 `{self.default_prefix}`로 설정됩니다.")
            guilds = read_json("guilds")
            guilds[guild_id] = guilds.get(guild_id, {})
            guilds[guild_id]["prefix"] = prefix
            write_json(guilds, "guilds")
        
    
    @commands.command(aliases=["load", "로드"], description="Load all/one of the bot's Cogs!")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    async def load_command(self, ctx, *cogs):
        async with ctx.typing():
            if not cogs:
                # load all cogs
                load_embed = discord.Embed(
                    title="Loaded All Cogs!",
                    colour=0x808080,
                    timestamp=ctx.message.created_at
                )
                for extension in os.listdir(f"{get_path()}/{self.foldername}"):
                    if extension.endswith(".py"):
                        try:
                            await self.bot.load_extension(f"{self.foldername}.{extension[:-3]}")
                            load_embed.add_field(
                                name=f"Loaded: `{extension}`",
                                value="\uFEFF",
                                inline=False
                            )
                        except Exception as e:
                            load_embed.add_field(
                                name=f"Failed to load: `{extension}`",
                                value=e,
                                inline=False
                            )
                await ctx.send(embed=load_embed)
            else:
                # load the specific cog(s)
                load_embed = discord.Embed(
                    title="Loaded the Specific Cog!",
                    colour=0x808080,
                    timestamp=ctx.message.created_at
                )
                for cog in cogs:
                    extension = f"{cog.lower()}.py"
                    if not os.path.exists(f"{get_path()}/{self.foldername}/{extension}"):
                        # if the file does not exist
                        load_embed.add_field(
                            name=f"Failed to load: `{extension}`",
                            value="This file does not exist",
                            inline=False
                        )
                    else:
                        try:
                            await self.bot.load_extension(f"{self.foldername}.{extension[:-3]}")
                            load_embed.add_field(
                                name=f"Loaded: `{extension}`",
                                value="\uFEFF",
                                inline=False
                            )
                        except Exception as e:
                            load_embed.add_field(
                                name=f"Failed to load: `{extension[:-3]}`",
                                value=e,
                                inline=False
                            )
                await ctx.send(embed=load_embed)
                
            
    @commands.command(aliases=["unload", "언로드"], description="Unload all/one of the bot's Cogs!")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    async def unload_command(self, ctx, *cogs):
        async with ctx.typing():
            if not cogs:
                # unload all cogs
                unload_embed = discord.Embed(
                    title="Unloaded All Cogs! (without `config.py`)",
                    colour=0x808080,
                    timestamp=ctx.message.created_at
                )
                for extension in os.listdir(f"{get_path()}/{self.foldername}"):
                    if extension.endswith(".py") and extension != "config.py":
                        try:
                            await self.bot.unload_extension(f"{self.foldername}.{extension[:-3]}")
                            unload_embed.add_field(
                                name=f"Unloaded: `{extension}`",
                                value="\uFEFF",
                                inline=False
                            )
                        except Exception as e:
                            unload_embed.add_field(
                                name=f"Failed to unload: `{extension}`",
                                value=e,
                                inline=False
                            )
                await ctx.send(embed=unload_embed)
            else:
                # unLoad the specific cog(s)
                unload_embed = discord.Embed(
                    title="Unloaded the Specific Cog!",
                    colour=0x808080,
                    timestamp=ctx.message.created_at
                )
                for cog in cogs:
                    extension = f"{cog.lower()}.py"
                    if not os.path.exists(f"{get_path()}/{self.foldername}/{extension}"):
                        # if the file does not exist
                        unload_embed.add_field(
                            name=f"Failed to unload: `{extension}`",
                            value="This file does not exist",
                            inline=False
                        )
                    elif extension != "config.py":
                        try:
                            await self.bot.unload_extension(f"{self.foldername}.{extension[:-3]}")
                            unload_embed.add_field(
                                name=f"Unloaded: `{extension}`",
                                value="\uFEFF",
                                inline=False
                            )
                        except Exception as e:
                            unload_embed.add_field(
                                name=f"Failed to unload: `{extension}`",
                                value=e,
                                inline=False
                            )
                await ctx.send(embed=unload_embed)        

                
    @commands.command(aliases=["reload", "리로드"], description="Reload all/one of the bot's Cogs!")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    async def reload_command(self, ctx, *cogs):
        async with ctx.typing():
            if not cogs:
                # reload all cogs
                reload_embed = discord.Embed(
                    title="Reloaded All Cogs!",
                    colour=0x808080,
                    timestamp=ctx.message.created_at
                )
                for extension in os.listdir(f"{get_path()}/{self.foldername}"):
                    if extension.endswith(".py"):
                        try:
                            await self.bot.reload_extension(f"{self.foldername}.{extension[:-3]}")
                            reload_embed.add_field(
                                name=f"Reloaded: `{extension}`",
                                value="\uFEFF",
                                inline=False
                            )
                        except Exception as e:
                            reload_embed.add_field(
                                name=f"Failed to reload: `{extension}`",
                                value=e,
                                inline=False
                            )
                await ctx.send(embed=reload_embed)
            else:
                # reload the specific cog(s)
                reload_embed = discord.Embed(
                    title="Reloaded the Specific Cog!",
                    colour=0x808080,
                    timestamp=ctx.message.created_at
                )
                for cog in cogs:
                    extension = f"{cog.lower()}.py"
                    if not os.path.exists(f"{get_path()}/{self.foldername}/{extension}"):
                        # if the file does not exist
                        reload_embed.add_field(
                            name=f"Failed to reload: `{extension}`",
                            value="This file does not exist",
                            inline=False
                        )
                    else:
                        try:
                            await self.bot.reload_extension(f"{self.foldername}.{extension[:-3]}")
                            reload_embed.add_field(
                                name=f"Reloaded: `{extension}`",
                                value="\uFEFF",
                                inline=False
                            )
                        except Exception as e:
                            reload_embed.add_field(
                                name=f"Failed to reload: `{extension[:-3]}`",
                                value=e,
                                inline=False
                            )
                await ctx.send(embed=reload_embed)
    
    
async def setup(bot):
    await bot.add_cog(Config(bot))