import os

import discord
from sentry_sdk import init
from discord.commands import Option
#from replit import db
from datetime import datetime
from helpers import open_account, fetch_user
from keepalive import keep_alive
from views import *
from asyncio import sleep, ensure_future, wait
from random import randint
from logging import getLogger, DEBUG, FileHandler, Formatter
from env import *
import pymongo
from pymongo import MongoClient

logger = getLogger('discord')
logger.setLevel(DEBUG)
handler = FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

init(
    SDKKEY,
    traces_sample_rate=1.0
)

bots = [878007103460089886, 625363818968776705, 574652751745777665]

intents = discord.Intents(message_content=True, messages=True, guilds=True, guild_messages=True)

bot = discord.AutoShardedBot(
    intents=intents, activity=discord.Game(name="Discord Bots | /invite"), owner_id = 586743480651350063
)

cluster = MongoClient(DBCONN)
bot.db = cluster["discord"]
bot.minecord = bot.db["minecord"]
bot.minecordclassic = bot.db["minecord-classic"]
bot.virtualfisher = bot.db["virtual-fisher"]
bot.stats = bot.db["statistics"]

minecord = bot.create_group("minecord", "Settings for Minecords")

stat_start = 1647338400

for filename in os.listdir("cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def on_ready():
    global bot
    print("Logged in as {0.user}".format(bot))
    print(f"{len(bot.guilds)} servers")
    
    bot.owner = await bot.fetch_user(bot.owner_id)
    await bot.owner.send("Online!")

    post1 = {"_id": 1, "success": 0, "trials": 0}
    bot.stats.insert_one(post1)

@bot.event
async def on_message(msg) -> None:
    if msg.author.id in bots:
        try:
            ctx = msg.channel
            msg.content = msg.content.lower()
            
            if msg.author.id == 878007103460089886:
                try:
                    try:
                        msg3 = msg
                        msg2 = await msg3.channel.fetch_message(
                            msg3.reference.message_id)
                        user = msg2.author
                    except:
                        user = msg.mentions[0]
                except:
                    return
                
                db = await fetch_user(msg.author, bot)
                
                if not (db["minecordclassic"]["mine"] or db["minecordclassic"]["fight"]
                        or db["minecordclassic"]["chop"] or db["minecordclassic"]["dragon"]):
                    return
        
                if ("you mined" in msg.content or "youmined" in msg.content) and ("in the nether" not in msg.content and "inthenether" not in msg.content) and db["minecordclassic"]["mine"]:
                    if db["minecordclassic"]["efficiency"]:
                        cooldown = 4
                    else:
                        cooldown = 5
                    command = "mine (classic)"
                elif ("you chopped" in msg.content or "youchopped" in msg.content) and ("in the nether" not in msg.content and "inthenether" not in msg.content) and db["minecordclassic"]["chop"]:
                    command = "chop"
                    if db["minecordclassic"]["efficiency"]:
                        cooldown = 45
                    else:
                        cooldown = 60
                elif ("you killed" in msg.content or "youkilled" in msg.content) and ("in the nether" not in msg.content and "inthenether" not in msg.content) and db["minecordclassic"]["fight"]:
                    cooldown = 40
                    command = "fight (classic)"
                    if db["minecordclassic"]["armor"] == 1:
                        cooldown = 40
                    elif db["minecordclassic"]["armor"] == 2:
                        cooldown = 37
                    elif db["minecordclassic"]["armor"] == 3:
                        cooldown = 35
                    elif db["minecordclassic"]["armor"] == 4:
                        cooldown = 30
                    elif db["minecordclassic"]["armor"] == 5:
                        cooldown = 25
                    elif db["minecordclassic"]["armor"] == 6:
                        cooldown = 20
                    if db["minecordclassic"]["efficiency"] == 1:
                        cooldown -= 10
                elif ("you dealt" in msg.content) and db["minecordclassic"]["dragon"]:
                    times = db["minecordclassic"]["dragon"]
                    cooldown = 60 * times
                    command = "enderdragon (classc)"
                elif ("you mined" in msg.content or "youmined" in msg.content) and ("in the nether" in msg.content or "inthenether" in msg.content) and db["minecordclassic"]["mine"]:
                    cooldown = 5
                    command = "nether mine (classic)"
                elif ("you chopped" in msg.content or "youchopped" in msg.content) and ("in the nether" in msg.content or "inthenether" in msg.content) and db["minecordclassic"]["chop"]:
                    cooldown = 60
                    command = "nether chop (classic)"
                elif  ("you killed" in msg.content or "youkilled" in msg.content) and ("in the nether" in msg.content or "inthenether" in msg.content) and db["minecordclassic"]["fight"]: 
                    cooldown = 45
                    command = "nether fight (classic)"
                else:
                    return
                response = db["minecordclassic"]["response"]
    
            if msg.author.id == 625363818968776705:
                
                try:
                    try:
                        msg2 = await msg.channel.fetch_message(
                            msg.reference.message_id)
                        user = msg2.author
                    except:
                        user = msg.mentions[0]
                except:
                    return
    
                if not (db["minecord"]["mine"] or db["minecord"]["fight"]
                        or db["minecord"]["chop"] or db["minecord"]["ed"]):
                    return
    
                if ("you mined" in msg.content or "youmined" in msg.content):
                    stats = bot.stats.find_one({"_id": 1})
                    stats["trials"] += 1
                    bot.stats.update_one({"_id":1}, {"$set": {"trials": stats["trials"]}})
                    if ("bosskey" in msg.content or "boss key" in msg.content):
                        stats["success"] += 1
                        bot.stats.update_one({"_id":1}, {"$set": {"success": stats["success"]}})
                    if db["minecord"]["mine"]:
                        if db["minecord"]["efficiency"] == 1:
                            cooldown = 4
                        else:
                            cooldown = 5
                        command = "mine"
    
                elif ("you chopped" in msg.content or "youchopped" in msg.content) and db["minecord"]["chop"]:
                    if db["minecord"]["efficiency"] == 1:
                        cooldown = 48
                    else:
                        cooldown = 60
                    command = "chop"
    
                elif ("you killed" in msg.content or "youkilled" in msg.content) and db["minecord"]["fight"]:
                    if db["minecord"]["efficiency"] == 1:
                        cooldown = 32
                    else:
                        cooldown = 45
                    command = "fight"
                else:
                    return
                response = db["minecord"]["response"]

            if msg.author.id == 574652751745777665:
                try:
                    try:
                        msg2 = await msg.channel.fetch_message(
                            msg.reference.message_id)
                        user = msg2.author
                    except:
                        user = msg.interaction.user
                except:
                    return
                
                for embed in msg.embeds:
                    embed = embed.to_dict()
    
                    try:
                        response = db["virtualfisher"]["response"]
                        if "You will now find more treasure for the next" in embed[
                                "description"] and db["virtualfisher"]["treasure"]:
                            minutes = int(embed["description"].split(" ")[10])
                            command = "treasure"
                            cooldown = minutes * 60
                            break
    
                        elif "You will now catch more fish for the next" in embed[
                                "description"] and db["virtualfisher"]["fish"] :
                            minutes = int(embed["description"].split(" ")[10])
                            command = "fish"
                            cooldown = minutes * 60
                            break
    
                        elif "You hired a worker for the next" in embed[
                                "description"] and "catches will automatically be added to your inventory." and db["virtualfisher"]["worker"] :
                            minutes = int(
                                embed["description"].split(" ")[8].split("**")[1]
                            )
                            command = "worker"
                            cooldown = minutes * 60
                            break
    
                        else:
                            continue
                        
                    except:
                        raise Exception
                
    
            
            try:
                response = response.replace("%", f"{user.mention}")
            except:
                pass
            try:
                response = response.replace("&", command)
            except:
                pass
            try:
                response = response.replace("$", f"{cooldown}")
            except:
                pass
            await sleep(cooldown)
    
            view = discord.ui.View()
            
            if randint(1, 10) == randint(1, 10):
                view.add_item(Vote())
                
            await ctx.send(response, view=view)
    
        except UnboundLocalError:
            pass
        
        except discord.errors.Forbidden:
            pass

        except:
            raise Exception

    if not(msg.author.bot):
        await open_account(msg.author, bot)
    
    if bot.user.id in msg.raw_mentions and "ping" in msg.content.lower():
        try:
            ping = int((bot.latencies[msg.guild.shard_id][1])*1000)
        except:
            ping = int(bot.latency*1000)
        embed = discord.Embed(title="Latency", description=f"**Gateway:** {ping} ms\n**Shard**: {msg.guild.shard_id}")

        if ping >= 1000:
            embed.color = discord.Color.red()
        elif ping >= 500:
            embed.color = discord.Color.orange()
        elif ping >= 200:
            embed.color = discord.Color.yellow()
        else:
            embed.color = discord.Color.green()

        if ping >= 100:
            view = discord.ui.View()
            view.add_item(Status())
            await msg.reply("Ping!", embed=embed, mention_author=False, view=view)
            return

        await msg.reply("Ping!", embed=embed, mention_author=False)

    if msg.author.id == 586743480651350063:
        if msg.content == "%reload":
            for filename in os.listdir("cogs"):
                if filename.endswith(".py"):
                    bot.reload_extension(f"cogs.{filename[:-3]}")
            await msg.channel.send("Reload success!")

    return

@bot.event
async def on_interaction(itx):
    await open_account(itx.user, bot)
    await bot.process_application_commands(itx)

@minecord.command(name="droprate",
                   description="Find the drop-rate of boss keys!")
async def droprate(ctx):
    success = (bot.stats.find_one({"_id": 1}))["success"]
    trials = (bot.stats.find_one({"_id": 1}))["trials"]
    bot.dispatch("application_command", ctx)
    embed = discord.Embed(title="Boss Key Drop Rates",
                          color=discord.Color.orange())
    embed.add_field(name="Boss Key Drops", value=success, inline=False)
    embed.add_field(name="Mines Recorded", value=trials, inline=False)
    embed.set_footer(
        text=
        f'Estimated chance of Boss Key drop: {round(success/(trials*100), 3)}% (1 in {round(trials/success)+1})'
    )
    embed.timestamp = datetime.now()
    await ctx.respond(embed=embed)

@minecord.command(name="setup", description="Setup for Minecord!")
async def setup(ctx):
    await ctx.defer(ephemeral=True)
    bot.dispatch("application_command", ctx)
    await open_account(ctx.author, bot)
    user = ctx.author
    view = Option1()
    em = discord.Embed(title="What are your settings for?",
                       color=ctx.author.color)
    em.set_footer(text=f"© Flash Assist 2022 | {int(bot.latency*1000)} ms | {ctx.author}")
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
        em.set_footer(text=f"© Flash Assist 2022 | {int(bot.latency*1000)} ms | {ctx.author}")
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
        em.set_footer(text=f"© Flash Assist 2022 | {int(bot.latency*1000)} ms | {ctx.author}")
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
        em.set_footer(text=f"© Flash Assist 2022 | {int(bot.latency*1000)} ms | {ctx.author}")

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
        em.set_footer(text=f"© Flash Assist 2022 | {int(bot.latency*1000)} ms | {ctx.author}")

        for child in opmin.children:
            child.disabled = True

        await ctx.interaction.edit_original_message(embed=em, view=opmin)
        return

    else:
        em = discord.Embed(title="Do you have efficiency?",
                           description="Yes | No",
                           color=ctx.author.color)
        em.timestamp = datetime.now()
        em.set_footer(text=f"© Flash Assist 2022 | {int(bot.latency*1000)} ms | {ctx.author}")

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
        em.set_footer(text=f"© Flash Assist 2022 | {int(bot.latency*1000)} ms | {ctx.author}")

        for child in op1.children:
            child.disabled = True
        em.timestamp = datetime.now()
        await ctx.interaction.edit_original_message(embed=em, view=op1)
        return

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
            embed.color = discord.Color.orange()
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
    await ctx.interaction.edit_original_message(embed=embed, view=view)


@bot.slash_command(
    name="terms",
    description="You can view our Terms of Service and Privacy Policy here, along with some additional information.")
async def terms(ctx):
    await ctx.defer()
    bot.dispatch("application_command", ctx)

    embed = discord.Embed(title="Flash Assist",
                          color=discord.Color.orange())
    embed.description = "[Terms of Service](https://flash-assist.squidsquidsquid.repl.co/terms)\n[Privacy Policy](https://flash-assist.squidsquidsquid.repl.co/privacy-policy)\n[Status Page](https://flashassist.statuspage.io/)\n[Website](https://flash-assist.squidsquidsquid.repl.co/)"
    embed.set_footer(text="Flash Assist is not affiliated with any of the Discord bots it supports.")
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
        
    try:
        response = response.replace("%",ctx.author.mention)
    except:
        pass
    try:
        response = response.replace("&","`command`")
    except:
        pass
    try:
        response = response.replace("$","3")
    except:
        pass
        
    success = discord.Embed(title="Success!", description = response, color=discord.Color.green())
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
    view.add_item(Invite4())
    view.add_item(Status())
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
bot.run(BOTTOKEN, reconnect=True)