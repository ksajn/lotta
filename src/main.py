""" Importing discord """

import discord
from discord import app_commands
from discord.ext import commands

""" Other """

import logging
import sqlite3

""" Importing libraries used to get token from .env file """

from dotenv import load_dotenv
import os

load_dotenv("./secrets/.env")
token = os.getenv('BOT_TOKEN')
tokend = os.getenv('BOT_TOKEND') 

""" Creating Client class """
class Lotta(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=discord.Intents.all()
        )

    async def setup_hook(self):
        coglist = [
            "config.imagechannel",
            "config.levelnotification",
            "info.help",
            "info.ping",
            "level.level",
            "listeners.threadCreator",
            "listeners.experienceListener",
            "roles.massrole",
            "logs.createLogs"
        ]
        for ext in coglist:
            try:
                await self.load_extension(ext)

            except Exception as e:
                log.exception(f'Failed to load extension {ext}.')

        await self.tree.sync()
        print('Successfully loaded all extensions')

""" Setup logging """

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = logging.getLogger(__name__)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')


if __name__ == "__main__":
    bot = Lotta()
    bot.remove_command(help)

    try:
        db = sqlite3.connect("data.sqlite")
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS exp(user_id INTEGER PRIMARY KEY, guild_id INTEGER, experience INTEGER, level INTEGER)")
        cursor.execute("CREATE TABLE IF NOT EXISTS threads(guild_id INTEGER PRIMARY KEY, channel_id INTEGER)")
        cursor.execute("CREATE TABLE IF NOT EXISTS expNotification(guild_id INTEGER PRIMARY KEY, boolean INTEGER)")

        cursor.close()
        db.close()

        print("Successfully connected to lotta's database")

    except Exception as e:
        print("Failed to connect to database. Error: " + e)

    try:
        print("lotta is running")
        bot.run(tokend, log_handler=handler)

    except Exception as err:
        print(f"error: {err}")
