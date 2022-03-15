import discord
from discord.ext import commands
from replit import db


class Ed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        def check(m):
            return m.channel == msg.channel and m.author.id == 878007103460089886

        msg.content = msg.content.lower()
        user = msg.author

        if msg.content in "m!ed" or msg.content in "m!enderdragon" or msg.content in "m!bf" or msg.content in "m!bossfight":

            try:
                msg2 = await self.bot.wait_for("message",
                                               check=check,
                                               timeout=20.0)
            except:
                pass

            try:
                embed = msg2.embeds[0].to_dict()
                damage = embed["description"].split("\n")[0].split(" ")[2]
                db[str(user.id)]["stats"]["damage"] = damage
                return
            except:
                pass

            try:
                embed = msg2.embeds[0].to_dict()
                damage = embed["description"].split(" ")[2]
                db[str(user.id)]["stats"]["damage"] = damage
            except:
                pass
            


def setup(bot):
    bot.add_cog(Ed(bot))  # register the cog
