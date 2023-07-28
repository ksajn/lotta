import discord
from discord import app_commands
from discord.ext import commands

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="List of all commands that are available and how to get help.")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="lotta's help",
            color=0x2b312b,
        )

        embed.add_field(
            name="bug report and support",
            value="to report a bug or get help DM `@kaynnig`."
        )
        embed.add_field(
            name="invite lotta",
            value="to invite lottta to your server, [click here](https://discord.com/api/oauth2/authorize?client_id=1123639728403660841&permissions=8&scope=applications.commands%20bot)",
            inline=False
        )
        embed.add_field(
            #inline=False,
            name="config commands",
            value="`levelnotification`, `threadconfig`"
        )
        embed.add_field(
            name="experience commands",
            value="`level`"
        )

        embed.add_field(
            name="info commands",
            value="`help`, `ping`"
        )

        await interaction.response.send_message(embed=embed)
async def setup(bot):
    await bot.add_cog(help(bot))