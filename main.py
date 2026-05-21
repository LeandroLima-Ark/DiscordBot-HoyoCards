import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
load_dotenv()

from utils.Embeds import (GenerateEmbed, GenerateView, GenerateList, GenerateCatchs)
from utils.HoyoAPI import (getCharacter, convert ,searchCharacter, LoadDatabaseCache, LoadClaimedCache)

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

@bot.command(name="roll", aliases=["r", "R"])
async def roll(ctx: commands.context):
    data = convert(getCharacter())
    await GenerateEmbed(ctx, bot, data)

@bot.command(name="view", aliases=["v", "V"])
async def view(ctx: commands.context, *,texto):
    search = searchCharacter(texto)
    if not search:
        return
    data = convert(search)
    await GenerateView(ctx, bot, data)

@bot.command(name="viewall", aliases=["vall", "va"])
async def viewall(ctx: commands.context, jogo: str = "all"):
    await GenerateList(ctx, jogo)

@bot.command()
async def favorites(ctx):
   await GenerateCatchs(ctx)

TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)