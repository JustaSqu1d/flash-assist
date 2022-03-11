import os

import discord
import sentry_sdk
from discord.commands import Option
from discord.ext import tasks
from replit import db

from helpers import changedatabase, open_account
from keepalive import keep_alive
from views import *

sentry_sdk.init(
    os.environ['SDKKEY'],
    traces_sample_rate=1.0
)

bots = [878007103460089886, 625363818968776705, 574652751745777665]

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = discord.AutoShardedBot(
    intents=intents, activity=discord.Game(name="Discord Bots | /setup"))

for filename in os.listdir("cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

@tasks.loop(seconds=10.0)
async def update_url():
    await changedatabase()

@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot))
    update_url.start()
    print(f"{len(bot.guilds)} servers")

@bot.event
async def on_message(msg) -> None:
    if msg.author.id in bots: 
        bot.dispatch("reminder", msg)
    elif msg.author.id == 586743480651350063 and msg.content == "%reload cogs":
        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                bot.reload_extension(f"cogs.{filename[:-3]}")
        await msg.channel.send("Reload success!")
    else:
        return

@bot.event
async def on_interaction(itx):
    await open_account(itx.user)
    await bot.process_application_commands(itx)

@bot.slash_command(
    name="terms",
    description="You can view our Terms of Service and Privacy Policy here.")
async def terms(ctx):
    await ctx.defer()
    bot.dispatch("application_command", ctx)
    embed = discord.Embed(title="Flash Assist Terms")
    embed.add_field(
        name="Links",
        value=
        "[Terms of Service](https://flash-assist.squidsquidsquid.repl.co/terms)\n[Privacy Policy](https://flash-assist.squidsquidsquid.repl.co/privacy-policy)",
        inline=False)
    await ctx.followup.send(embed=embed)


@bot.slash_command(name="setup", description="Change your settings!")
async def setup(ctx):
    await ctx.defer(ephemeral=True)
    bot.dispatch("application_command", ctx)
    await open_account(ctx.author)
    user = ctx.author
    view = Option1()
    em = discord.Embed(title="What are your settings for?",
                       color=ctx.author.color)
    em.set_footer(text=f"© just a squid#5483 2022 | m!help | {ctx.author}")
    await ctx.followup.send(embed=em, view=view)

    timedout = await view.wait()

    if timedout:
        for child in view.children:
            child.disabled = True
        await ctx.interaction.edit_original_message(view=view)
        return

    if view.value:

        em = discord.Embed(title="Do you have efficiency?",
                           description="Yes | No",
                           color=ctx.author.color)
        em.set_footer(text=f"© just a squid#5483 2022 | m!help | {ctx.author}")
        op1 = Option2()
        await ctx.interaction.edit_original_message(embed=em, view=op1)

        timedout = await op1.wait()

        if timedout:
            for child in op1.children:
                child.disabled = True
            await ctx.interaction.edit_original_message(view=op1)
            return

        if op1.value:
            db[str(user.id)]["efficiency"] = 1

        else:
            db[str(user.id)]["efficiency"] = 0

        opar = OptionAr()

        em = discord.Embed(title="What armor do you have?",
                           color=ctx.author.color)

        em.set_footer(text=f"© just a squid#5483 2022 | %setup | {ctx.author}")
        await ctx.interaction.edit_original_message(embed=em, view=opar)

        timedout = await opar.wait()

        if timedout:
            for child in opar.children:
                child.disabled = True
            await ctx.interaction.edit_original_message(view=opar)
            return

        db[str(user.id)]["armor"] = opar.value

        em = discord.Embed(
            title="What is your Ender Dragon cooldown (answer in minutes)?",
            description="Enter a number!",
            color=ctx.author.color)
        em.set_footer(text=f"© just a squid#5483 2022 | m!help | {ctx.author}")

        opmin = OptionMin()

        await ctx.interaction.edit_original_message(embed=em, view=opmin)

        timedout = await opmin.wait()

        if timedout:
            for child in opmin.children:
                child.disabled = True
            await ctx.interaction.edit_original_message(view=opmin)
            return

        db[str(user.id)]["armor"] = opmin.value

        em = discord.Embed(title="Setup Complete!",
                           color=discord.Color.green())
        em.set_footer(text=f"© just a squid#5483 2022 | m!help | {ctx.author}")

        for child in opmin.children:
            child.disabled = True
        await ctx.interaction.edit_original_message(view=opmin)

        await ctx.interaction.edit_original_message(embed=em, view=opmin)
        return

    else:
        em = discord.Embed(title="Do you have efficiency?",
                           description="Yes | No",
                           color=ctx.author.color)
        em.set_footer(text=f"© just a squid#5483 2022 | m!help | {ctx.author}")

        op1 = Option2()
        await ctx.interaction.edit_original_message(embed=em, view=op1)

        timedout = await op1.wait()

        if timedout:
            for child in op1.children:
                child.disabled = True
            await ctx.interaction.edit_original_message(view=op1)
            return

        if op1.value:
            db[str(user.id)]["efficiency2"] = 1

        else:
            db[str(user.id)]["efficiency2"] = 0

        em = discord.Embed(title="Setup Complete!",
                           color=discord.Color.green())
        em.set_footer(text=f"© just a squid#5483 2022 | m!help | {ctx.author}")

        for child in op1.children:
            child.disabled = True

        await ctx.interaction.edit_original_message(embed=em, view=op1)
        return


@bot.slash_command(
    name="config",
    description="Edit what commands you want to be reminded upon!!")
async def config(ctx):
    bot.dispatch("application_command", ctx)
    embed = discord.Embed(title="Reminder Control Panel!",
                          description="Green: ON\nRed: OFF")
    view = Toggles(ctx)
    await ctx.respond(embed=embed, view=view, ephemeral=True)
    to = await view.wait()
    while not (to):
        if not (view.value):
            view = TogglesCl(ctx)
            await ctx.interaction.edit_original_message(view=view)
        else:
            view = Toggles(ctx)
            await ctx.interaction.edit_original_message(view=view)
        to = await view.wait()


@bot.slash_command(name="droprate",
                   description="Find the drop-rate of boss keys!")
async def droprate(ctx):
    bot.dispatch("application_command", ctx)
    embed = discord.Embed(title="Boss Key Drop Rates",
                          color=discord.Color.orange())
    embed.add_field(name="Boss Key Drops", value=db["success"], inline=False)
    embed.add_field(name="Mines Recorded", value=db["trials"], inline=False)
    embed.set_footer(
        text=
        f'Estimated chance of Boss Key drop: {round((db["success"]/db["trials"]*100), 3)}%'
    )
    await ctx.respond(embed=embed)


@bot.slash_command(name="response",
                   description="Use your own custom reminder messages!")
async def _response(ctx, response: Option(
    str, description="Use custom response messages!", required=True)):
    bot.dispatch("application_command", ctx)
    if "%" not in response:
        failed = discord.Embed(
            title="Missing Arguments!",
            description=
            "Make your own custom reminder with `/response`\nPlease use the following format in your message:\n**Put `%` on where you want you to be mentioned.**\n`&` for the name.^\n`$` for the cooldown.^\n\n*^optional*"
        )
        failed.add_field(
            name="Example",
            value=
            f"`/response % & elasped (cd:$)`\nBecomes\n\n{ctx.author.mention} command elapsed (cd:5)"
        )
        await ctx.respond(embed=failed)
        return
    user = ctx.author
    db[str(user.id)]["response"] = response
    success = discord.Embed(title="Success!", color=discord.Color.green())
    await ctx.respond(embed=success)


@bot.slash_command(name="invite", description="Invite me to join your server!")
async def invite(ctx):
    bot.dispatch("application_command", ctx)
    embed = discord.Embed(title="Invite me. :)", color=discord.Color.orange())
    embed.description = ""
    view = discord.ui.View()
    view.add_item(Invite())
    view.add_item(Invite2())
    await ctx.respond(embed=embed, view=view)


@bot.slash_command(name="guide", description="A guide for the bots we support")
async def guide(ctx):
    bot.dispatch("application_command", ctx)
    embed = discord.Embed(
        title="Guide",
        description="**[Minecord](https://just-a-squid.gitbook.io/minecord-1/v/minecord/)**\n**[Virtual Fisher](https://virtualfisher.com/guide)**",
        color=discord.Color.orange()
    )
    embed.set_footer("Flash Assist is not affiliated with any of the Discord bots it supports.")
    await ctx.respond(embed=embed)


keep_alive()
bot.run(os.environ['BOTTOKEN'])
