import discord


class VFVerify(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.Cog.listener()
    async def on_message(self, message):
        try:
            message.content = message.content.lower()
            if message.author.id != 574652751745777665:
                return
            embed = message.embeds[0].to_dict()
            if "Anti-bot" not in embed["title"]:
                return

            em = discord.Embed(
                title="A Wild Verification Appeared!", color=discord.Color.red()
            )
            await message.reply(embed=em, tts=True, mention_author=False)
        except:
            pass


def setup(bot):
    bot.add_cog(VFVerify(bot))
