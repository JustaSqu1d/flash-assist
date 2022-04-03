import discord
from discord.ext import commands


class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        msg.content = msg.content.lower()

        if 'anti bot check. complete this addition:' in msg.content and msg.author.id in [
                625363818968776705, 878007103460089886
        ]:
            x = msg.content.split("`")[1]
            x = x.split(" ")
            y = int(x[0])
            z = int(x[2])
            final = y + z
            em = discord.Embed(
                title=f"m!verify {final}".upper(),
                description=f"Type the command `m!verify {final}`!",
                color=discord.Color.brand_red())

            user = msg.mentions[0]
            await user.send(f"""{msg.jump_url}""")
            for i in range(0, 5):

                await msg.channel.send(user.mention, embed=em)

        if msg.author.id == 878007103460089886 and "you failed the verification and have been banned for 24 hours." in msg.content:

            await msg.channel.send(
                "Join this server to appeal for an unban! discord.gg/XgcUHqtcd2"
            )


def setup(bot):
    bot.add_cog(Verify(bot))  # register the cog
