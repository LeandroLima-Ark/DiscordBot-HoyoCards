import discord
from discord.ext import commands
from utils.database_functions import (user_exists, create_user, ClaimCharacter)
from utils.HoyoAPI import (verifyOwner)
from utils.Emojis import (Elements, Paths, Jade)

class HeartButton(discord.ui.View):
    def __init__(self, character):
        super().__init__(timeout=None)
        self.character = character

    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        emoji="❤️"
    )
    async def heart(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        # pega quem clicou
        usuario = interaction.user

        if not user_exists(usuario.id):
            create_user(usuario)

        character = self.character

        result = ClaimCharacter(usuario.id, character["game"], character["id"], interaction.guild.id)

        if result["success"]:
            for item in self.children:
                item.disabled = True
            await interaction.message.edit(
                view=self
            )
            self.stop()

            await interaction.response.send_message(
                f"{usuario.mention} capturou **{character["name"]}** ❤️"
            )
        else:
            return

async def GenerateEmbed(ctx: commands.Context, bot, id):
    
    name = id["name"]
    url  = id["image"]
    game = id["game"]

    rarity = id["rarity"]
    element = id["element"]
    
    Side = id["weapon"] if game == "Genshin Impact" else id["path"]

    field = "Weapon" if game == "Genshin Impact" else "Path" 

    Element_emoji = Elements.get(element, "") 
    Path_emoji = Paths.get(Side, "")

    Emb = discord.Embed()
    Emb.title = name
    Emb.description = (
        f"**Rank**: {rarity} ⭐\n"
        f"**Element**: {element} {Element_emoji} \n"
        f"**{field}**: {Side} {Path_emoji} \n"
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