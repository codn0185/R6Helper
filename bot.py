# https://discord.com/api/oauth2/authorize?client_id=1050716394792169562&permissions=137439291456&scope=bot


import discord
from discord.ext import commands
import asyncio
from pathlib import Path
import sys

from Utils.Json import *


def run(TOKEN):
    print(f"# python-{sys.version}")
    print(f"# discord-{discord.__version__}")
    print()

    DEFAULT_PREFIX = "!"

    def get_prefix(bot, message):
        if not message.guild:
            return commands.when_mentioned_or(DEFAULT_PREFIX)(bot, message)
        guild_id = str(message.guild.id)
        filename = "guilds"
        if is_json(filename):
            guilds = read_json(filename)
            guilds[guild_id] = guilds.get(guild_id, {})
            guilds[guild_id]["prefix"] = guilds[guild_id].get("prefix", DEFAULT_PREFIX)
        prefix = guilds[guild_id]["prefix"]
        return commands.when_mentioned_or(prefix)(bot, message)


    async def setup(bot):
        foldername = 'Cogs'
        for filename in os.listdir(f"{Path(__file__).parents[0]}/{foldername}"):
            if filename.endswith(".py"):
                try:
                    await bot.load_extension(f"{foldername}.{filename[:-3]}")
                except Exception as e:
                    print(f'{filename} 로드 실패:\n{e}\n')


    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix=get_prefix, intents=intents, case_insensitive=True)

    asyncio.run(setup(bot))


    @bot.event
    async def on_ready():
        print('------------------------------')
        print('연결 중입니다')
        print(f'봇={bot.user.name}로 연결 중')
        print('연결이 완료되었습니다')
        print('------------------------------')
        await bot.change_presence(status=discord.Status.online, activity=None)

    bot.run(TOKEN)
    
    
if __name__ == "__main__":
    pass