import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
load_dotenv()

from utils.Embeds import (GenerateEmbed)
from utils.HoyoAPI import (getCharacter, LoadDatabaseCache, LoadClaimedCache)

perm = discord.Intents.all()
perm.emojis = True
bot = commands.Bot("$", intents=perm)

# ####################################################################

@bot.event
async def on_ready():
    refresh_cache.start()
    await LoadClaimedCache()
    print("Bot inicializado com sucesso!")

@tasks.loop(minutes=60)
async def refresh_cache():
    await LoadDatabaseCache()

# ###################################################################
# Commands
# ###################################################################

@bot.command()
async def w(ctx: commands.context):
    data = getCharacter()
    await GenerateEmbed(ctx, bot, data)

TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)