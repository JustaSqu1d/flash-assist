import discord


class Verify(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot: discord.Bot = bot

    @discord.Cog.listener()
    async def on_message(self, msg: discord.Message) -> None:
        msg.content = msg.content.lower()
        msg.content = msg.content.replace(" ", "")

        if "antibotcheck.completethisaddition:" in msg.content and msg.author.id in [
            625363818968776705,
            878007103460089886,
        ]:
            x = msg.content.split("`")[1]
            x = x.split("+")
            y = int(x[0])
            z = int(x[1])
            final = y + z
            em = discord.Embed(
                title=f"m!verify {final}".upper(),
                description=f"Type the command `m!verify {final}`!",
                color=discord.Color.brand_red(),
            )

            user = msg.mentions[0]
            try:
                await user.send(f"""{msg.jump_url}""")
            except discord.HTTPException:
                await msg.channel.send(
                    "Missing Permissions. Check your discord settings to allow direct messages."
                )

            for i in range(0, 5):

                await msg.channel.send(user.mention, embed=em)

        if (
            msg.author.id == 878007103460089886
            and "youfailedtheverificationandhavebeenbannedfor24hours." in msg.content
        ):

            await msg.channel.send(
                "Join this server to appeal for an unban! discord.gg/XgcUHqtcd2"
            )


def setup(bot: discord.Bot) -> None:
    bot.add_cog(Verify(bot))
