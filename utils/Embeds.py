import discord
from discord.ext import commands
from utils.database_functions import (SearchAllCharacters)
from utils.Views import (HeartButton, PageView)
from utils.HoyoAPI import (verifyOwner)
from utils.Emojis import (Elements, Paths, Jade)

async def GenerateEmbed(ctx: commands.Context, bot, id):
    
    name = id["name"]
    url  = id["image"]
    game = id["game"]
    rarity = id["rarity"]
    element = id["element"]
    trace = id["trace"]

    field = "Weapon" if game == "Genshin Impact" else "Path" 

    Element_emoji = Elements.get(element, "") 
    Path_emoji = Paths.get(trace, "")

    Emb = discord.Embed()
    Emb.title = name
    Emb.description = (
        f"**Rank**: {rarity} ⭐\n"
        f"**Element**: {element} {Element_emoji} \n"
        f"**{field}**: {trace} {Path_emoji} \n"
        "\n"
        f"**Value**: 200 {Jade} \n"
        "\n"
        f"**{game}**"
    )

    Emb.set_image(url=url)

    view = HeartButton(id)

    owner = verifyOwner(ctx.guild.id, id["id"])
    if owner:
        user = bot.get_user(int(owner["user_id"]))
        Emb.set_footer(text=f"Capturado por {user.display_name}", icon_url=user.display_avatar.url)
    else:
        Emb.set_footer(text="não capturado")

    await ctx.send(embed=Emb, view=view)

async def GenerateView(ctx: commands.Context, bot, id):
    name = id["name"]
    url  = id["image"]
    game = id["game"]
    rarity = id["rarity"]
    element = id["element"]
    trace = id["trace"]
    field = "Weapon" if game == "Genshin Impact" else "Path" 
    Element_emoji = Elements.get(element, "") 
    Path_emoji = Paths.get(trace, "")
    Emb = discord.Embed()
    Emb.title = name
    Emb.description = (
        f"**Rank**: {rarity} ⭐\n"
        f"**Element**: {element} {Element_emoji} \n"
        f"**{field}**: {trace} {Path_emoji} \n"
        "\n"
        f"**Value**: 200 {Jade} \n"
        "\n"
        f"**{game}**"
    )
    Emb.set_image(url=url)
    owner = verifyOwner(ctx.guild.id, id["id"])
    if owner:
        user = bot.get_user(int(owner["user_id"]))
        Emb.set_footer(text=f"Capturado por {user.display_name}", icon_url=user.display_avatar.url)
    else:
        Emb.set_footer(text="não capturado")
    await ctx.send(embed=Emb)

async def GenerateList(ctx: commands.Context):
    lista = SearchAllCharacters()
    texto = []

    for i in lista:
        nome = i["name"]
        texto.append(nome)

    if not texto:
        return
    
    itensPage = 25
    page = []
    for i in range(0, len(texto), itensPage):
        pierce = texto[i:i + itensPage]
        itens = "\n".join(pierce)
        page.append(itens)

    Emb = discord.Embed()
    Emb.title = "Lista de personagens:"
    Emb.description = page[0]

    view = PageView(page)

    await ctx.send(embed=Emb, view=view)