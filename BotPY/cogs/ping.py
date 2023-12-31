import discord
from discord.ext import commands
from discord import app_commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="ping", description="Affiche le ping du bot")
    async def ping_slash(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Le Ping du bot est de {round(self.bot.latency * 1000)} ms", ephemeral=False)
    
    @ping_slash.error
    async def say_error(self, interaction: discord.Interaction, error):
        if isinstance(error, commands.CheckFailure):
            await interaction.response.send_message("Tu n'as pas les permissions !", ephemeral=True)
        else:
            await interaction.response.send_message(f"Une erreur s'est produite : {error}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Ping(bot))