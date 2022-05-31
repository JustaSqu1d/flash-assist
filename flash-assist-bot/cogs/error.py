import discord, sys
from discord.ext import commands
from datetime import datetime
from views import Status

class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_error(self, event = None, args = None, kwargs = None):

        embed = discord.Embed(title = f"Error at {event}", color=discord.Color.red())
        embed.add_field(name="Args", value = args)
        embed.add_field(name="Kwargs", value = kwargs)
        embed.set_footer(text = sys.exc_info())
        embed.timestamp = datetime.now()
        
        await self.bot.owner.send(embed=embed)

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, exception):

        if isinstance(exception,discord.HTTPException):
            await ctx.respond("Missing Permissions. Re-invite the bot with `/invite`.")

        embed = discord.Embed(title = "A superduper rare error occured.",description="Meanwhile, we have begun to debug this bug. Everything should work iceman perfect. You can also check our status page if there is an outage.")
        view = discord.ui.View()
        view.add_item(Status())
        if ctx.response.is_done():
            await ctx.followup.send(embed=embed, view=view)
        else:
            await ctx.respond(embed=embed, view=view)

        error = discord.Embed(title=f"Error at {ctx.command.qualified_name}!", color=discord.Color.red())
        error.add_field(name="User", value = f"{ctx.author} ({ctx.author.id})")
        try:
            error.add_field(name="Guild/Channel", value = f"{ctx.guild.name}/{ctx.channel.mention}")
        except:
            pass
        error.add_field(name="Message", value = f"{ctx.message}")
        error.add_field(name="Command/Component", value = f"{ctx.interaction.is_command()}/{ctx.interaction.is_component()}")
        error.add_field(name="Permissions", value = f"{ctx.interaction.permissions}")
        error.add_field(name="Data", value = f"{ctx.interaction.data}")
        error.add_field(name="Exception", value = f"{exception}: {exception.__traceback__}")
        error.set_footer(text = sys.exc_info())
        error.timestamp = datetime.now()
        await self.bot.owner.send(embed=error)

def setup(bot):
    bot.add_cog(Error(bot))