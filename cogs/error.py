import discord
from discord.ext import commands
from replit import db


class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_error(self, event, args, kwargs):
        pass

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, exception):
        pass

def setup(bot):
    bot.add_cog(Error(bot))