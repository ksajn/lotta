import discord
from discord import app_commands
from discord.ext import commands
import sqlite3

class imagechannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.choices(
        choice=[
            discord.app_commands.Choice(name='Create', value=1),
            discord.app_commands.Choice(name='Delete', value=2),
        ]
    )
    @app_commands.checks.has_permissions(manage_guild = True)
    @app_commands.command(name='imagechannel', description='configure channel where bot will create threads and only allow to send images (URLs arent supported)')
    async def imagechannel(self, interaction: discord.Interaction, choice: int, channel: discord.TextChannel):
        try:
            db = sqlite3.connect("data.sqlite")
            cursor = db.cursor()
            cursor.execute(f"SELECT channel_id FROM threads WHERE guild_id = {interaction.guild.id}")
            result = cursor.fetchone()

            if choice == 1:
                if result == None:
                    cursor.execute(f'INSERT INTO threads(guild_id) VALUES({interaction.guild.id})')

                cursor.execute(f"UPDATE threads SET channel_id = {channel.id} WHERE guild_id = {interaction.guild.id}")
                cursor.close()
                db.commit()
                db.close()
                    
                await interaction.response.send_message(f"Successfully set {channel.id} as channel where bot'll create threads and only allow to send images.")
            
            elif choice == 2:
                if result == None:
                    cursor.execute(f"INSERT INTO threads(guild_id, channel_id) VALUES({interaction.guild.id}, 0)")
                cursor.execute(f'UPDATE threads SET channel_id = 0 WHERE guild_id = {interaction.guild.id}')
                cursor.close()
                db.commit()
                db.close()

                await interaction.response.send_message(f"Sucessfully deleted image channel.")

        except Exception:
            await interaction.response.send_message(f"An error encountered! You probably don't have enough permissions to run this command.")
        
        
        

async def setup(bot):
    await bot.add_cog(imagechannel(bot))