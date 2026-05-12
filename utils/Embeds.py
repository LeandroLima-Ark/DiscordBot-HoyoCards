import discord
from discord.ext import commands
from utils.database_functions import (user_exists, create_user, ClaimCharacter, get_favorites)

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

        result = ClaimCharacter(usuario.id, character["game"], character["id"])

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

async def GenerateEmbed(ctx: commands.Context,id, nome, URL, game):
    Emb = discord.Embed()
    Emb.title = nome
    Emb.description = game

    Emb.set_image(url=URL)

    view = HeartButton(id)

    await ctx.send(embed=Emb, view=view)

async def GenerateFav(ctx):
    embed = discord.Embed(
        title=f"{ctx.author.name} Favorites ❤️",
        color=discord.Color.red()
    )

    favorites = get_favorites(ctx.author.id)
    
    # sem favoritos
    if len(favorites) == 0:
        embed.description = "Você não possui personagens favoritados."
    else:
        texto = ""
        for character in favorites:
            texto += f"• {character}\n"
        embed.description = texto

    await ctx.send(embed=embed)