import discord
from discord.ext import commands

import sqlite3

class ThreadCreator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.author.bot:
                return

            db = sqlite3.connect("data.sqlite")
            cursor = db.cursor()

            cursor.execute("SELECT channel_id FROM threads WHERE guild_id = ?", (message.guild.id,))
            result = cursor.fetchone()

            if result is None or 0:
                return

            if message.channel.id == result[0]:
                print(message.content)
                print(message.type)
                if message.attachments:
                    await message.create_thread(name="Komentarze")
                    await message.add_reaction("❤️")
                if str(message.content).endswith(".png"):
                    await message.create_thread(name="Komentarze")
                    await message.add_reaction("❤️")
                elif str(message.content).endswith(".jpg"):
                    await message.create_thread(name="Comments")
                    await message.add_reaction("❤️")

                elif str(message.content).endswith(".jpeg"):
                    await message.create_thread(name="Comments")
                    await message.add_reaction("❤️")
                if not message.attachments:
                    if str(message.content).endswith(".png"):
                        await message.create_thread(name="Komentarze")
                        await message.add_reaction("❤️")
                    elif str(message.content).endswith(".jpg"):
                        await message.create_thread(name="Comments")
                        await message.add_reaction("❤️")

                    elif str(message.content).endswith(".jpeg"):
                        await message.create_thread(name="Comments")
                        await message.add_reaction("❤️")
                    else:
                        await message.delete()
            else:
                return

            cursor.close()
            db.commit()
            db.close()
        except Exception as e:
            print(e)

async def setup(bot):
    try:
        await bot.add_cog(ThreadCreator(bot))
    except Exception as e:
        print(e)