import discord
from discord import app_commands
from discord.ext import commands

class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='ping', description='sends bot latency in ms')
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed = discord.Embed(
            title = "lotta", #'estetyka'
            description=f"**Pong!** 🏓 \n Lotta's latency is **{round(self.bot.latency * 1000)}**ms",
            color=0x2b312b
        ))

async def setup(bot):
    await bot.add_cog(ping(bot))