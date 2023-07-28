import discord
from discord import app_commands
from discord.ext import commands
import time
import asyncio

class massrole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.choices(
        choice=[
            discord.app_commands.Choice(name='Add', value=1),
            discord.app_commands.Choice(name='Remove', value=2),
        ]
    )
    @app_commands.command(name='massrole', description='Add/remove roles from all guild users')
    async def massrole(self, interaction: discord.Interaction, choice: int, role: discord.Role):
        try:
            print(role)
            print(interaction.guild.members)

            if interaction.user.guild_permissions.manage_roles:
                print(role)
                print(interaction.guild.members)

                await interaction.response.send_messages(f"It might take a while.")

                if choice == 1:
                    for user in interaction.guild.members:
                        await user.add_roles(role, reason=None)
                        time.sleep(1)

                    await interaction.response.send_message(f"Successfully added role `<@{role.id}>` to all members.")
                elif choice == 2:
                    for user in interaction.guild.members:
                        await user.remove_roles(role, reason=None)
                        time.sleep(1)

                    await interaction.response(f"Successfully removed role `<@{role.id}>` from all members.")

            else:
                raise discord.Forbidden(f"{interaction.user} doesn't have the manage_guild permission.")

        except Exception:
            await interaction.response.send_message(f"An error encountered! You probably don't have enough permissions to run this command.")


async def setup(bot):
    await bot.add_cog(massrole(bot))