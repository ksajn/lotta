import random

import discord
from discord.ext import commands
from discord import app_commands

import random

import sqlite3

class level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='level', description='chceck you actual level')
    async def level(self, interaction: discord.Interaction):

        db = sqlite3.connect("data.sqlite")
        cursor = db.cursor()

        cursor.execute("SELECT experience FROM exp WHERE user_id = ?", (interaction.user.id,))
        result = cursor.fetchone() 

        if result == None:
            cursor.execute("INSERT INTO exp (user_id, experience, level) VALUES (?, ?, ?)", (interaction.user.id, 1, 1))

        cursor.execute("SELECT experience FROM exp WHERE user_id = ?", (interaction.user.id,))
        exp = cursor.fetchone()

        cursor.execute("SELECT level FROM exp WHERE user_id = ?", (interaction.user.id,))
        level = cursor.fetchone()

        requiredExp = 40 * int(level[0]) * 1.1

        embed = discord.Embed(
            title="lotta",
            description=f"Hey, {interaction.user}! You have earned **{level[0]}** level(s) \nTo get new level, you need to collect **{int(requiredExp - int(exp[0]))}** more experience points!",
            color=0x2b312b

        )

        db.commit()
        cursor.close()
        db.close()

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(level(bot))




