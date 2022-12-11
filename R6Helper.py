import os

import bot
try:
    from constants.gitignore import data
    TOKEN = data["TOKEN"]
except:
    TOKEN = os.environ['TOKEN']
    
    
bot.run(TOKEN)