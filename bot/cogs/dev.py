import discord


class Dev(discord.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot

    @discord.Cog.listener()
    async def on_message(self, msg: discord.Message) -> None:
        if (
            msg.author.id == 625363818968776705
            and "Successfully joined clan `Valar Morghulis`".lower() in msg.content
        ):
            roles = await msg.guild.fetch_roles()
            for role in roles:
                if role.id == 882120373582315540:
                    member_role = role
                    break
            await msg.mentions[0].add_roles(member_role)


def setup(bot: discord.Bot):
    bot.add_cog(Dev(bot))
