import discord
from discord.ext import commands
from discord import app_commands

class RoleReact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_message_id = None 
        self.emoji_to_role = {
            "🟤":1172181582170300477,
            "⚪":1172181646213120010,
            "🔵":1172188196180865078,
            "🔴":1172188051972300860,
            "🟡":1172188011597930496
        }

    @app_commands.command(name="role", description="Créer un message pour choisir des rôles.")
    @app_commands.default_permissions(administrator=True)
    async def role_slash(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        question = "Veuillez choisir une reaction pour avoir un role"
        message = await interaction.followup.send(question, ephemeral=False)
        self.role_message_id = message.id
        for emoji in self.emoji_to_role:
            await message.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        role = self.get_role_from_payload(payload)
        if role is not None:
            await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        role = self.get_role_from_payload(payload)
        if role is not None:
            member = self.bot.get_guild(payload.guild_id).get_member(payload.user_id)
            if member is not None:
                await member.remove_roles(role)

    def get_role_from_payload(self, payload):
        if payload.message_id != self.role_message_id:
            return None
        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return None
        role_id = self.emoji_to_role.get(str(payload.emoji))
        if role_id is None:
            return None
        return guild.get_role(role_id)

    @role_slash.error
    async def say_error(self, interaction: discord.Interaction, error):
        if isinstance(error, commands.CheckFailure):
            await interaction.response.send_message("Tu n'as pas les permissions !", ephemeral=True)
        else:
            await interaction.response.send_message(f"Une erreur s'est produite : {error}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(RoleReact(bot))
