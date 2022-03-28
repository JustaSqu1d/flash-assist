import discord
from discord.ext import commands
from helpers import in_progress
from replit import db
import sys


class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.id != self.bot.owner_id:
            return
        try:
            if msg.content == "%current":
                await msg.channel.send(in_progress+"")
                
        except:
            self.bot.dispatch("error", "on_message", msg)

def setup(bot):
    bot.add_cog(Dev(bot))