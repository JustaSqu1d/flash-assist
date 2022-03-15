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
            
            msg3 = None

            async for message in msg.channel.history(limit=10):
                if "you dealt" in message.content and msg.author in msg.mentions and message.author.id == 878007103460089886:
                    msg3 = message.content

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
            
            try:
                print(msg3.content)
            except:
                pass
            


def setup(bot):
    bot.add_cog(Ed(bot))  # register the cog
