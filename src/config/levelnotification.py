import discord
from discord import app_commands
from discord.ext import commands
import sqlite3


class levelnotification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.choices(
        choice=[
            discord.app_commands.Choice(name='Turn on', value=1),
            discord.app_commands.Choice(name='Turn off', value=2),
        ]
    )

    @app_commands.command(name='levelnotification', description="configure level notifications, by default it's turned on.")
    async def threadconfig(self, interaction: discord.Interaction, choice: int):
        try:
            db = sqlite3.connect("data.sqlite")
            cursor = db.cursor()

            if not interaction.user.guild_permissions.manage_guild:
                raise discord.Forbidden(f"{interaction.user} doesn't have the manage_guild permission.")
            
            cursor.execute(f"SELECT boolean FROM expNotification WHERE guild_id = {interaction.guild.id}")
            result = cursor.fetchone()

            if result == None:
                cursor.execute(f'INSERT INTO expNotification(guild_id, boolean) VALUES({interaction.guild.id}, 1)')

            if choice == 1:
                cursor.execute(f'UPDATE expNotification SET boolean = 1 WHERE guild_id = {interaction.guild.id}')
                await interaction.response.send_message(f"{interaction.guild.name}'s level notifications have been turned on.")
            elif choice == 2:
                cursor.execute(f'UPDATE expNotification SET boolean = 0 WHERE guild_id = {interaction.guild.id}')
                await interaction.response.send_message(f"{interaction.guild.name}'s level notifications have been turned off.")


            cursor.close()
            db.commit()
            db.close()

        except discord.Forbidden:
            await interaction.response.send_message(f"{interaction.user} doesn't have the manage_guild permission.")  

        except Exception:
            await interaction.response.send_message(f"An error encountered! You probably don't have enough permissions to run this command.")
async def setup(bot):
    await bot.add_cog(levelnotification(bot))