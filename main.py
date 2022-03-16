import os

import discord
import sentry_sdk
from discord.commands import Option
from replit import db
from datetime import datetime
from helpers import open_account
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
    intents=intents, activity=discord.Game(name="Discord Bots | /setup")
)

minecord = bot.create_group("minecord", "Settings for Minecords")

stat_start = 1647338400

for filename in os.listdir("cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot))
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
        
    elif msg.content == "<@!836581672811495465>" or msg.content == "<@!836581672811495465>\n":
        ping = int((bot.latencies[msg.guild.shard_id][1])*1000)   
        embed = discord.Embed(title="Latency", description=f"**Gateway:** {ping} ms\n**Shard**: {msg.guild.shard_id}")

        if ping >= 1000:
            embed.color = discord.Color.red()
        elif ping >= 500:
            embed.color = discord.Color.orange()
        elif ping >= 200:
            embed.color = discord.Color.yellow()
        else:
            embed.color = discord.Color.green()

        await msg.reply("Ping!", embed=embed, mention_author=False)

    else:
        return

@bot.event
async def on_interaction(itx):
    await open_account(itx.user)
    await bot.process_application_commands(itx)

@minecord.command(name="droprate",
                   description="Find the drop-rate of boss keys!")
async def droprate(ctx):
    bot.dispatch("application_command", ctx)
    embed = discord.Embed(title="Boss Key Drop Rates",
                          color=discord.Color.orange())
    embed.add_field(name="Boss Key Drops", value=db["success"], inline=False)
    embed.add_field(name="Mines Recorded", value=db["trials"], inline=False)
    embed.set_footer(
        text=
        f'Estimated chance of Boss Key drop: {round((db["success"]/db["trials"]*100), 3)}% (1 in {round(db["trials"]/db["success"])+1})'
    )
    embed.timestamp = datetime.now()
    await ctx.respond(embed=embed)

@minecord.command(name="setup", description="Setup for Minecord!")
async def setup(ctx):
    await ctx.defer(ephemeral=True)
    bot.dispatch("application_command", ctx)
    await open_account(ctx.author)
    user = ctx.author
    view = Option1()
    em = discord.Embed(title="What are your settings for?",
                       color=ctx.author.color)
    em.set_footer(text=f"© Flash Assist 2022 | /invite | {ctx.author}")
    em.timestamp = datetime.now()
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
        em.set_footer(text=f"© Flash Assist 2022 | /invite | {ctx.author}")
        em.timestamp = datetime.now()
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
        em.timestamp = datetime.now()
        em.set_footer(text=f"© Flash Assist 2022 | %setup | {ctx.author}")
        await ctx.interaction.edit_original_message(embed=em, view=opar)

        timedout = await opar.wait()

        if timedout:
            for child in opar.children:
                child.disabled = True
            await ctx.interaction.edit_original_message(view=opar)
            return

        db[str(user.id)]["armor"] = opar.value

        em = discord.Embed(
            title="What is your Ender Dragon cooldown (In minutes)?",
            description="Select a number!",
            color=ctx.author.color)
        em.timestamp = datetime.now()
        em.set_footer(text=f"© Flash Assist 2022 | /invite | {ctx.author}")

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
        em.timestamp = datetime.now()
        em.set_footer(text=f"© Flash Assist 2022 | /invite | {ctx.author}")

        for child in opmin.children:
            child.disabled = True
        await ctx.interaction.edit_original_message(view=opmin)

        await ctx.interaction.edit_original_message(embed=em, view=opmin)
        return

    else:
        em = discord.Embed(title="Do you have efficiency?",
                           description="Yes | No",
                           color=ctx.author.color)
        em.timestamp = datetime.now()
        em.set_footer(text=f"© Flash Assist 2022 | /invite | {ctx.author}")

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
        em.set_footer(text=f"© Flash Assist 2022 | /invite | {ctx.author}")

        for child in op1.children:
            child.disabled = True
        em.timestamp = datetime.now()
        await ctx.interaction.edit_original_message(embed=em, view=op1)
        return

@minecord.command(name="stats", description="Your Minecord statistics!")
async def stats(ctx):
    await ctx.defer(ephemeral=True)
    bot.dispatch("application_command", ctx)
    await open_account(ctx.author)
    user = ctx.author
    embed = discord.Embed(title=f"{user.name}'s Statistics",
                       color=discord.Color.random())
    try:
        all_damage = 0
        for damage in db[str(user.id)]["damages"]:
            all_damage += damage
        total_fights = len(db[str(user.id)]["damages"])
        avg_damage = all_damage/total_fights
        avg_damage = round(avg_damage, 2)
        
    except:
        db[str(user.id)]["damages"] = []
        all_damage, avg_damage, total_fights = 0, 0, 0

    embed.add_field(name = "Ender Dragon (Classic)", value = f"Total Damage: {all_damage}\nAverage Damage: {avg_damage}\nTotal Fights: {total_fights}", inline = False)
    #TODO embed.add_field(name = "")
    embed.set_footer(text="Statistics since")
    embed.timestamp = datetime.fromtimestamp(stat_start)
    await ctx.followup.send(embed=embed)
    

@bot.slash_command(
    name="config",
    description="Edit what commands you want to be reminded upon!!")
async def config(ctx):
    bot.dispatch("application_command", ctx)
    embed = discord.Embed(title="Reminder Control Panel",
                          description="**Green:** ON\n**Red:** OFF")
    view = Toggles(ctx)
    embed.set_footer(text="Click the buttons to toggle between modes!")
    embed.timestamp = datetime.now()
    await ctx.respond(embed=embed, view=view, ephemeral=True)
    view.value = "Minecord"
    to = await view.wait()
    while not (to):
        if view.value == "Minecord Classic":
            view = TogglesCl(ctx)
            embed.color = discord.Color.white()
            await ctx.interaction.edit_original_message(view=view)
        elif view.value == "Minecord":
            view = Toggles(ctx)
            embed.color = discord.Color.yellow()
            await ctx.interaction.edit_original_message(view=view)
        elif view.value == "Virtual Fisher":
            view = TogglesVf(ctx)
            embed.color = discord.Color.blue()
            await ctx.interaction.edit_original_message(view=view)
            
        to = await view.wait()
    for child in view.children:
        child.disabled = True
    embed.set_footer(text="Buttons timed-out. Use the command again.")
    await ctx.interaction.edit_original_message(view=view)


@bot.slash_command(
    name="terms",
    description="You can view our Terms of Service and Privacy Policy here.")
async def terms(ctx):
    await ctx.defer()
    bot.dispatch("application_command", ctx)

    embed = discord.Embed(title="Boss Key Drop Rates",
                          color=discord.Color.orange())
    embed.add_field(name="Boss Key Drops", value=db["success"], inline=False)
    embed.add_field(name="Mines Recorded", value=db["trials"], inline=False)
    embed.set_footer(
        text=
        f'Estimated chance of Boss Key drop: {round((db["success"]/db["trials"]*100), 3)}% (1 in {round(db["trials"]/db["success"])})'
    )
    embed.timestamp = datetime.now()
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
        failed.timestamp = datetime.now()
        
        await ctx.respond(embed=failed)
        return
    user = ctx.author
    response = discord.utils.escape_mentions(response)
    db[str(user.id)]["response"] = response
    success = discord.Embed(title="Success!", color=discord.Color.green())
    success.timestamp = datetime.now()
    await ctx.respond(embed=success)


@bot.slash_command(name="invite", description="Invite me to join your server!")
async def invite(ctx):
    bot.dispatch("application_command", ctx)
    embed = discord.Embed(title="Flash Assist", description = "Flash Assist is a Discord bot that reminds you to use commands when the command's cooldown has elapsed or ended.\nThis service covers a couple bots, but the coverage for more bots is coming soon!\nFeatures includes custom reminders along with friendly UI for easy customization!", color=discord.Color.orange())
    embed.description = ""
    view = discord.ui.View()
    view.add_item(Invite())
    view.add_item(Invite2())
    view.add_item(Invite3())
    await ctx.respond(embed=embed, view=view)


@bot.slash_command(name="guide", description="A guide for the bots we support.")
async def guide(ctx):
    bot.dispatch("application_command", ctx)
    embed = discord.Embed(
        title="Guide",
        description="**[Minecord](https://just-a-squid.gitbook.io/minecord-1/v/minecord/)**\n**[Virtual Fisher](https://virtualfisher.com/guide)**",
        color=discord.Color.orange()
    )
    embed.timestamp = datetime.now()
    embed.set_footer(text="Flash Assist is not affiliated with any of the Discord bots it supports.")
    await ctx.respond(embed=embed)


keep_alive()
bot.run(os.environ['BOTTOKEN'], reconnect=True)