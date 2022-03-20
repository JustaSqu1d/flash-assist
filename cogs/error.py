import discord
from discord.ext import commands
from replit import db
from datetime import datetime


class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_error(self, event, args, kwargs):

        embed = discord.Embed(titele = f"Error at {event}", color=discord.Color.red())
        embed.add_field(name="Args", value = args)
        embed.add_field(name="Kwargs", value = kwargs)
        embed.timestamp = datetime.now()
        
        await self.bot.owner.send(embed=embed)

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, exception):
        embed = discord.Embed(title = "A superduper rare error occured.",description="Meanwhile, we have begun to debug this bug. Everything should work iceman perfect. You can also check our status page if there is an outage.")
        view = discord.ui.View()
        view.add_item(Status())
        if ctx.response.is_done():
            await ctx.followup.send(embed=embed, view=view)
        else:
            await ctx.respond(embed=embed, view=view)

        error = discord.Embed(title=f"Error at {ctx.command.qualified_name}!")
        error.add_field(name="User", value = f"{ctx.author}")
        error.add_field(name="Guild/Channel", value = f"{ctx.guild.name}/{ctx.channel.mention}")
        error.add_field(name="Message", value = f"{ctx.message}")
        error.add_field(name="Command/Component", value = f"{ctx.interaction.is_command()}/{ctx.interaction.is_component()}")
        error.add_field(name="Permissions", value = f"{ctx.interaction.permissions}")
        error.add_field(name="Data", value = f"{ctx.interaction.data}")
        error.timestamp = datetime.now()
        await bot.owner.send(embed=embed)

def setup(bot):
    bot.add_cog(Error(bot))