from discord.ext import commands

class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.id != self.bot.owner_id:
            return

def setup(bot):
    bot.add_cog(Dev(bot))