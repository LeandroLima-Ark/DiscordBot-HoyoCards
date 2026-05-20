import discord
from utils.database_functions import (user_exists, create_user, ClaimCharacter)

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
        
class PageView(discord.ui.View):
    def __init__(self, paginas):
        super().__init__(timeout=180)
        self.paginas = paginas
        self.pagina_atual = 0

    async def atualizar_pagina(self, interaction: discord.Interaction, nova_pagina: int):
        self.pagina_atual = nova_pagina
        
        embed_atual = interaction.message.embeds[0]
        
        embed_atual.description = self.paginas[self.pagina_atual]
        embed_atual.set_footer(text=f"Página {self.pagina_atual + 1} de {len(self.paginas)}")
        
        await interaction.response.edit_message(embed=embed_atual, view=self)
    
    # Botão de Voltar (emoji de seta para a esquerda)
    @discord.ui.button(emoji="⬅️", style=discord.ButtonStyle.primary)
    async def botao_voltar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.pagina_atual > 0:
            await self.atualizar_pagina(interaction, self.pagina_atual - 1)
        else:
            await interaction.response.defer()
    
    # Botão de Avançar (emoji de seta para a direita)
    @discord.ui.button(emoji="➡️", style=discord.ButtonStyle.primary)
    async def botao_avancar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.pagina_atual < len(self.paginas) - 1:
            await self.atualizar_pagina(interaction, self.pagina_atual + 1)
        else:
            await interaction.response.defer()