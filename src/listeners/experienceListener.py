import random
import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from discord import app_commands
import sqlite3
import time

class ExperienceListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldowns = {}  # Dictionary to track cooldowns

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if len(message.content) < 5:
            return

        if message.author.id in self.cooldowns:
            cooldown_time = self.cooldowns[message.author.id]
            if time.time() - cooldown_time < 20:
                return

        self.cooldowns[message.author.id] = time.time()

        exp = random.randint(1, 5)

        db = sqlite3.connect("data.sqlite")
        cursor = db.cursor()

        cursor.execute("SELECT experience FROM exp WHERE user_id = ?", (message.author.id,))
        result = cursor.fetchone()

        if result == None:
            cursor.execute("INSERT INTO exp (user_id, experience, level) VALUES (?, ?, ?)", (message.author.id, 1, 1))

        cursor.execute("UPDATE exp SET experience = experience + ? WHERE user_id = ?", (exp, message.author.id))

        db.commit()

        cursor.execute("SELECT experience FROM exp WHERE user_id = ?", (message.author.id,))
        exp = cursor.fetchone()

        cursor.execute("SELECT level FROM exp WHERE user_id = ?", (message.author.id,))
        level = cursor.fetchone()
        
        cursor.execute("SELECT boolean FROM expNotification WHERE guild_id = ?", (message.guild.id,))
        doSend = cursor.fetchone()
            
        if doSend == None:
                cursor.execute("INSERT INTO expNotification VALUES (?, 1)", (message.guild.id,))
        
        
        requiredExp = 40 * int(level[0]) * 1.1

        if int(exp[0]) > requiredExp:
            cursor.execute("UPDATE exp SET level = level + 1 WHERE user_id = ?", (message.author.id,))
            db.commit()

            cursor.execute("SELECT level FROM exp WHERE user_id = ?", (message.author.id,))
            level = cursor.fetchone()
            if int(doSend[0]) == 1:
                await message.channel.send(f"{message.author.mention}, you have leveled up! Your level is now {level[0]}!")
                    
        else:
            return False

        db.commit()
        cursor.close()
        db.close()

async def setup(bot):
    await bot.add_cog(ExperienceListener(bot))




