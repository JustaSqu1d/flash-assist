import os
import discord
from discord.ext import tasks
from sentry_sdk import init
from datetime import datetime, timedelta
from helpers import open_account, fetch_user, convert_to_seconds
from views import *
from asyncio import sleep
from random import randint
from logging import getLogger, DEBUG, FileHandler, Formatter
from time import time
from motor.motor_asyncio import AsyncIOMotorClient
from bson import encode
from bson.raw_bson import RawBSONDocument
import nest_asyncio

nest_asyncio.apply()

logger = getLogger("discord")
logger.setLevel(DEBUG)
handler = FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

init(os.environ.get("SDKKEY"), traces_sample_rate=1.0)

bots = [878007103460089886, 574652751745777665]

intents = discord.Intents(
    message_content=True, messages=True, guilds=True, guild_messages=True, members=True
)

bot = discord.AutoShardedBot(
    intents=intents,
    activity=discord.Game(name="Discord Bots | /config"),
    owner_id=586743480651350063,
)

cluster = AsyncIOMotorClient(
    os.environ.get("DBCONN")
)
bot.db = cluster["discord"]
bot.minecordclassic = bot.db["minecord-classic"]
bot.virtualfisher = bot.db["virtual-fisher"]
bot.stats = bot.db["statistics"]
bot.events = bot.db["events"]

bot.session = {}

minecord = bot.create_group("minecord", "Minecord")
virtualfisher = bot.create_group("virtualfisher", "Virtual Fisher")
event = bot.create_group("event", "Event settings")

bot.load_extension("cogs", recursive=True)


@tasks.loop(seconds=15)
async def update_events() -> None:
    async for event in bot.events.find({}):
        try:
            if event["end_time"] < time():

                guild = await bot.events.find_one({"_id": str(event["_id"])})
                leaderboard = guild["participants"]

                total = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
                description = ""

                index = 1

                for entry in total:
                    player = await bot.get_or_fetch_user(int(entry[0]))
                    description += f"**{index}. {player.name}#{player.discriminator}** - {entry[1]}\n"

                    if index == 10:
                        break
                    else:
                        index += 1

                embed = discord.Embed(
                    title="Final Event Leaderboard!",
                    description=description,
                    color=discord.Color.brand_red(),
                )
                embed.set_footer(text="Event ended")
                channel = await bot.fetch_channel(event["channel"])
                await channel.send(embed=embed)
                await bot.events.find_one_and_delete({"_id": event["_id"]})
        except:
            pass


@tasks.loop(hours=1)
async def clear_session() -> None:
    bot.session = {}


@bot.event
async def on_ready() -> None:
    global bot
    print("Logged in as {0.user}".format(bot))
    print(f"{len(bot.guilds)} servers")
    # update_events.start()
    clear_session.start()
    bot.owner = await bot.get_or_fetch_user(bot.owner_id)
    await bot.owner.send("Online!")


@bot.event
async def on_message(msg: discord.Message) -> None:
    if msg.author.id in bots:
        try:

            msg.content = msg.content.lower()

            if msg.author.id == 878007103460089886:
                try:
                    try:
                        msg3 = msg
                        msg2 = await msg3.channel.fetch_message(
                            msg3.reference.message_id
                        )
                        user = msg2.author
                    except:
                        user = msg.mentions[0]
                except:
                    return

                await open_account(user, bot)
                db = await fetch_user(user, bot)

                if not (
                    db["minecordclassic"]["mine"]
                    or db["minecordclassic"]["fight"]
                    or db["minecordclassic"]["chop"]
                    or db["minecordclassic"]["ed"]
                ):
                    return

                if (
                    ("you mined" in msg.content or "youmined" in msg.content)
                    and (
                        "in the nether" not in msg.content
                        and "inthenether" not in msg.content
                    )
                    and db["minecordclassic"]["mine"]
                ):
                    if db["minecordclassic"]["efficiency"]:
                        cooldown = 4
                    else:
                        cooldown = 5
                    command = "mine"
                elif (
                    ("you chopped" in msg.content or "youchopped" in msg.content)
                    and (
                        "in the nether" not in msg.content
                        and "inthenether" not in msg.content
                    )
                    and db["minecordclassic"]["chop"]
                ):
                    command = "chop"
                    if db["minecordclassic"]["efficiency"]:
                        cooldown = 45
                    else:
                        cooldown = 60
                elif (
                    ("you killed" in msg.content or "youkilled" in msg.content)
                    and (
                        "in the nether" not in msg.content
                        and "inthenether" not in msg.content
                    )
                    and db["minecordclassic"]["fight"]
                ):
                    cooldown = 40
                    command = "fight"
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
                    if db["minecordclassic"]["efficiency"]:
                        cooldown -= 10
                elif ("you dealt" in msg.content) and db["minecordclassic"]["ed"]:
                    times = db["minecordclassic"]["ed"]
                    cooldown = 60 * times
                    command = "enderdragon"
                elif (
                    ("you mined" in msg.content or "youmined" in msg.content)
                    and ("in the nether" in msg.content or "inthenether" in msg.content)
                    and db["minecordclassic"]["mine"]
                ):
                    cooldown = 5
                    command = "nether mine"
                elif (
                    ("you chopped" in msg.content or "youchopped" in msg.content)
                    and ("in the nether" in msg.content or "inthenether" in msg.content)
                    and db["minecordclassic"]["chop"]
                ):
                    cooldown = 60
                    command = "nether chop"
                elif (
                    ("you killed" in msg.content or "youkilled" in msg.content)
                    and ("in the nether" in msg.content or "inthenether" in msg.content)
                    and db["minecordclassic"]["fight"]
                ):
                    cooldown = 45
                    command = "nether fight"
                else:
                    return
                response = db["minecordclassic"]["response"]

            elif msg.author.id == 574652751745777665:

                try:
                    try:
                        msg2 = await msg.channel.fetch_message(msg.reference.message_id)
                        user = msg2.author
                    except:
                        user = msg.interaction.user
                except:
                    return

                await open_account(user, bot)
                db = await fetch_user(user, bot)

                if db["virtualfisher"]["fish"]:

                    for rows in msg.components:

                        for component in rows.children:

                            if "Fish Again" == component.label:

                                for embed in msg.embeds:

                                    embed = embed.to_dict()
                                    try:

                                        author = embed["author"]["name"]

                                        if (
                                            f"{author}{msg.guild.id}"
                                            in bot.session.keys()
                                        ):
                                            user = await msg.guild.fetch_member(
                                                bot.session[author]
                                            )
                                            break

                                        potential_people = [
                                            item
                                            for item in msg.guild.members
                                            if item.display_name == author
                                        ]
                                        if len(potential_people) > 1:

                                            embed = discord.Embed(
                                                title="Confirmation Button",
                                                color=discord.Colour.brand_green(),
                                            )

                                            class Confirmation(discord.ui.View):
                                                def __init__(self) -> None:
                                                    super().__init__(timeout=15)
                                                    self.interaction = None
                                                    self.author = None

                                                @discord.ui.button(
                                                    label="Confirm",
                                                    row=0,
                                                    style=discord.ButtonStyle.green,
                                                )
                                                async def callback(
                                                    self,
                                                    button: discord.ui.Button,
                                                    interaction: discord.Interaction,
                                                ):
                                                    if (
                                                        interaction.user
                                                        not in potential_people
                                                    ):
                                                        return
                                                    self.author = interaction.user
                                                    self.interaction = interaction
                                                    await interaction.response.send(
                                                        "Confirmed", ephemeral=True
                                                    )
                                                    self.stop()

                                            confirmation = Confirmation()

                                            await msg.channel.send(
                                                embed=embed, view=confirmation
                                            )

                                            timedout = await confirmation.wait()
                                            if timedout:
                                                return
                                            else:
                                                user = confirmation.author
                                                bot.session.update(
                                                    {f"{author}{msg.guild.id}": user.id}
                                                )
                                        else:
                                            user = potential_people[0]
                                        db = await fetch_user(user, bot)
                                        if db["virtualfisher"]["fish"]:

                                            command = "Fish"
                                            cooldown = db["virtualfisher"]["cooldown"]

                                        break
                                    except Exception as e:
                                        raise e

                for embed in msg.embeds:
                    embed = embed.to_dict()

                    try:
                        response = db["virtualfisher"]["response"]
                        if (
                            "You will now find more treasure for the next"
                            in embed["description"]
                            and db["virtualfisher"]["treasure"]
                        ):
                            minutes = int(embed["description"].split(" ")[10])
                            command = "treasure"
                            cooldown = minutes * 60
                            break

                        elif (
                            "You will now catch more fish for the next"
                            in embed["description"]
                            and db["virtualfisher"]["fish"]
                        ):
                            minutes = int(embed["description"].split(" ")[10])
                            command = "fishing"
                            cooldown = minutes * 60
                            break

                        elif (
                            "You hired a worker for the next" in embed["description"]
                            and "catches will automatically be added to your inventory."
                            and db["virtualfisher"]["worker"]
                        ):
                            minutes = int(
                                embed["description"].split(" ")[8].split("**")[1]
                            )
                            command = "worker"
                            cooldown = minutes * 60
                            break

                        else:
                            continue
                    except:
                        pass

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

            view.add_item(
                discord.ui.Button(
                    label="Teleport to Message",
                    style=discord.ButtonStyle.link,
                    url=msg.jump_url,
                )
            )

            await msg.reply(response, view=view, delete_after=cooldown)

        except UnboundLocalError:
            pass

        except discord.errors.Forbidden:
            pass

    if not (msg.author.bot):
        await open_account(msg.author, bot)

    if bot.user.id in msg.raw_mentions and "ping" in msg.content.lower():
        try:
            ping = int((bot.latencies[msg.guild.shard_id][1]) * 1000)
        except:
            ping = int(bot.latency * 1000)
        try:
            embed = discord.Embed(
                title="Latency",
                description=f"**Gateway:** {ping} ms\n**Shard**: {msg.guild.shard_id}",
            )
        except:
            embed = discord.Embed(
                title="Latency", description=f"**Gateway:** {ping} ms\n**Shard**: n/a"
            )

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
            for filename in os.listdir("/cogs"):
                if filename.endswith(".py"):
                    bot.reload_extension(f"cogs.{filename[:-3]}")
            await msg.channel.send("Reload success!")

    return


@bot.event
async def on_interaction(itx: discord.Interaction) -> None:
    await open_account(itx.user, bot)
    await bot.process_application_commands(itx)


@minecord.command(name="setup", description="Setup for Minecord Classic!")
async def setup(ctx: discord.ApplicationContext) -> None:
    await ctx.defer(ephemeral=True)

    await open_account(ctx.author, bot)

    em = discord.Embed(
        title="Do you have efficiency?",
        description="Yes | No",
        color=ctx.author.color,
    )
    em.set_footer(
        text=f"?? Flash Assist 2022 | {int(bot.latency*1000)} ms | {ctx.author}"
    )
    em.timestamp = datetime.now()
    op1 = Option2()
    await ctx.interaction.edit_original_message(embed=em, view=op1)

    timedout = await op1.wait()

    if timedout:
        for child in op1.children:
            child.disabled = True
        await ctx.interaction.edit_original_message(view=op1)
        return

    await bot.minecordclassic.update_one(
        {"_id": ctx.author.id}, {"$set": {"efficiency": op1.value}}
    )

    opar = OptionAr()

    em = discord.Embed(title="What armor do you have?", color=ctx.author.color)
    em.timestamp = datetime.now()
    em.set_footer(
        text=f"?? Flash Assist 2022 | {int(bot.latency*1000)} ms | {ctx.author}"
    )
    await ctx.interaction.edit_original_message(embed=em, view=opar)

    timedout = await opar.wait()

    if timedout:
        for child in opar.children:
            child.disabled = True
        await ctx.interaction.edit_original_message(view=opar)
        return

    await bot.minecordclassic.update_one(
        {"_id": ctx.author.id}, {"$set": {"armor": opar.value}}
    )

    em = discord.Embed(
        title="What is your Ender Dragon cooldown (In minutes)?",
        description="Select a number!",
        color=ctx.author.color,
    )
    em.timestamp = datetime.now()
    em.set_footer(
        text=f"?? Flash Assist 2022 | {int(bot.latency*1000)} ms | {ctx.author}"
    )

    opmin = OptionMin()

    await ctx.interaction.edit_original_message(embed=em, view=opmin)

    timedout = await opmin.wait()

    if timedout:
        for child in opmin.children:
            child.disabled = True
        await ctx.interaction.edit_original_message(view=opmin)
        return

    await bot.minecordclassic.update_one(
        {"_id": ctx.author.id}, {"$set": {"ed": opmin.value}}
    )

    em = discord.Embed(
        title="Setup Complete!",
        description="You can edit the commands you want to be reminded upon with `/config`!",
        color=discord.Color.green(),
    )
    em.timestamp = datetime.now()
    em.set_footer(
        text=f"?? Flash Assist 2022 | {int(bot.latency*1000)} ms | {ctx.author}"
    )

    for child in opmin.children:
        child.disabled = True

    await ctx.interaction.edit_original_message(embed=em, view=opmin)
    return


@bot.slash_command(
    name="config", description="Edit what commands you want to be reminded upon!!"
)
async def config(ctx: discord.ApplicationContext) -> None:
    await ctx.defer(ephemeral=True)
    embed = discord.Embed(
        title="Reminder Control Panel", description="**Green:** ON\n**Red:** OFF"
    )
    view = TogglesCl(ctx)
    embed.set_footer(text="Click the buttons to toggle between modes!")
    embed.timestamp = datetime.now()
    await ctx.respond(embed=embed, view=view)
    to = await view.wait()
    while not (to):
        if view.value == "Virtual Fisher":
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
    description="You can view our Terms of Service and Privacy Policy here, along with some additional information.",
)
async def terms(ctx: discord.ApplicationContext) -> None:
    await ctx.defer()

    embed = discord.Embed(title="Flash Assist", color=discord.Color.orange())
    embed.description = "[Terms of Service](https://flash-assist.glitch.me/tos.html)\n[Privacy Policy](https://flash-assist.glitch.me/policy.html)\n[Status Page](https://flashassist.statuspage.io/)\n[Website](https://flash-assist.glitch.me/)"
    embed.set_footer(
        text="Flash Assist is not affiliated with any of the Discord bots it supports."
    )
    embed.timestamp = datetime.now()
    await ctx.respond(embed=embed)


@bot.slash_command(
    name="response", description="Use your own custom reminder messages!"
)
async def response1(
    ctx,
    response: discord.Option(
        str, description="Use custom response messages!", required=True
    ),
    bot2: discord.Option(
        str,
        name="bot",
        description="Choose the bot you want to edit reminder responses for.",
        choices=["Minecord Classic", "Virtual Fisher"],
        required=True,
    ),
) -> None:

    if "%" not in response:
        failed = discord.Embed(
            title="Missing Arguments!",
            description="Make your own custom reminder with `/response`\nPlease use the following format in your message:\n**Put `%` on where you want you to be mentioned.**\n`&` for the name.^\n`$` for the cooldown.^\n\n*^optional*",
        )
        failed.add_field(
            name="Example",
            value=f"`/response % & elasped (cd:$)`\nBecomes\n\n{ctx.author.mention} command elapsed (cd:5)",
        )
        failed.timestamp = datetime.now()

        await ctx.respond(embed=failed)
        return

    user = ctx.author
    response = discord.utils.escape_mentions(response)
    bot2 = bot2.lower().replace(" ", "-")
    bot.db[bot2].update_one({"_id": ctx.author.id}, {"$set": {"response": response}})

    try:
        response = response.replace("%", user.mention)
    except:
        pass
    try:
        response = response.replace("&", "`command`")
    except:
        pass
    try:
        response = response.replace("$", "3")
    except:
        pass

    success = discord.Embed(
        title="Success!", description=response, color=discord.Color.green()
    )
    success.timestamp = datetime.now()
    await ctx.respond(embed=success)


@bot.slash_command(name="invite", description="Invite me to join your server!")
async def invite(ctx: discord.ApplicationContext) -> None:

    embed = discord.Embed(
        title="Flash Assist",
        description="Flash Assist is a Discord bot that reminds you to use commands when the command's cooldown has elapsed or ended.\nThis service covers a couple bots, but the coverage for more bots is coming soon!\nFeatures includes custom reminders along with friendly UI for easy customization!",
        color=discord.Color.orange(),
    )
    embed.description = ""
    view = discord.ui.View()
    view.add_item(Invite())
    view.add_item(Invite2())
    view.add_item(Invite3())
    view.add_item(Invite4())
    view.add_item(Status())
    await ctx.respond(embed=embed, view=view)


@bot.slash_command(name="guide", description="A guide for the bots we support.")
async def guide(ctx: discord.ApplicationContext) -> None:

    embed = discord.Embed(
        title="Guide",
        description="**[Virtual Fisher](https://virtualfisher.com/guide)**",
        color=discord.Color.orange(),
    )
    embed.timestamp = datetime.now()
    embed.set_footer(
        text="Flash Assist is not affiliated with any of the Discord bots it supports."
    )
    await ctx.respond(embed=embed)


@event.command(name="start", description="Start a Minecord event for your server!")
async def start(
    ctx,
    channel: discord.Option(
        discord.TextChannel, "Choose a channel to send the event to."
    ),
) -> None:
    if not (ctx.user.guild_permissions.manage_guild):
        await ctx.respond("Missing Manage Server Permissions!")
        return

    guild = await bot.events.find_one({"_id": str(ctx.guild.id)})
    if guild is not None:
        await ctx.respond("Only one event at a time!")
        return
    event = Event()
    await ctx.send_modal(event)
    timedout = await event.wait()
    if not (timedout):
        return
    else:
        timeevent = await convert_to_seconds(event.value)
        if timeevent == "Invalid time unit!":
            await event.interaction.followup.send("Invalid time unit(s)!")
            return
        if timeevent > 60:
            await event.interaction.followup.send("Event is too short!")
            return

        start_time = time()
        end_time = start_time + timeevent
        await bot.events.insert_one(
            {
                "_id": str(ctx.guild.id),
                "start_time": start_time,
                "end_time": end_time,
                "channel": channel.id,
                "participants": RawBSONDocument(encode({str(ctx.user.id): 0})),
            }
        )
        try:
            await ctx.guild.create_scheduled_event(
                name="Minecord Event",
                start_time=discord.utils.utcnow() + timedelta(seconds=5),
                end_time=datetime.now() + timedelta(seconds=timeevent),
                location=channel.mention,
            )
        except discord.HTTPException:
            await event.interaction.followup.send(
                'I am missing permissions. Use the "Add to server" button on my profile to correct the permissions.'
            )
            return

        try:
            await bot.fetch_channel(channel.id)
        except:
            await event.interaction.followup.send(
                "Invalid channel! Make sure I have permissions to send messages in that channel."
            )
        await event.interaction.followup.send(
            f"Event started! Results will be displayed in {channel.mention}! Make sure I have permissions to send messages and embed links in {channel.mention}!"
        )


@event.command(name="end", description="End a event for your server!")
async def end(ctx: discord.ApplicationContext) -> None:
    if not (ctx.user.guild_permissions.manage_guild):
        await ctx.respond("Missing Manage Server Permissions!")
        return
    if (await bot.events.find_one({"_id": str(ctx.guild.id)})) is not None:
        await ctx.respond("There are no events!")
        return

    await bot.events.update_one(
        {"_id": str(ctx.guild.id)}, {"$set": {"end_time": time()}}
    )

    await ctx.respond("Event ended!")


@event.command(name="leaderboard", description="View the event leaderboard!")
async def leaderboard(ctx: discord.ApplicationContext) -> None:

    await ctx.defer()
    guild = await bot.events.find_one({"_id": str(ctx.guild.id)})
    if guild is None:
        await ctx.respond("There is no ongoing event!")
        return
    leaderboard = guild["participants"]

    total = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
    description = ""

    index = 1

    for entry in total:
        player = await bot.get_or_fetch_user(int(entry[0]))
        description += (
            f"**{index}. {player.name}#{player.discriminator}** - {entry[1]}\n"
        )

        if index == 10:
            break
        else:
            index += 1

    embed = discord.Embed(
        title="Event Leaderboard!", description=description, color=discord.Color.green()
    )
    embed.timestamp = datetime.fromtimestamp(
        await bot.events.find_one({"_id": str(ctx.guild.id)})["end_time"]
    )
    embed.set_footer(text="Event ends at")
    await ctx.respond(embed=embed)


@event.command(name="info", description="View the event info!")
async def info(ctx: discord.ApplicationContext) -> None:

    await ctx.defer()
    if (await bot.events.find_one({"_id": str(ctx.guild.id)})) is None:
        await ctx.respond("There is no ongoing event!")
        return
    description = "Players will gain event points for participating in the event.\n\nMines: 1 Point\nFights: 5 Points\nChops: 9 Points\nNote: All commands must be used in the event server!"
    embed = discord.Embed(
        title="Event Info!", description=description, color=discord.Color.green()
    )
    embed.timestamp = datetime.fromtimestamp(
        await bot.events.find_one({"_id": str(ctx.guild.id)})["end_time"]
    )
    embed.set_footer(text="Event ends at")
    await ctx.respond(embed=embed)


@virtualfisher.command(
    name="cooldown", description="Change the cooldown for the Virtual Fisher bot!"
)
async def cooldown(
    ctx: discord.ApplicationContext,
    cooldown: discord.Option(
        float,
        description="Your current cooldown",
        required=True,
        min_value=2,
        max_value=15,
    ),
) -> None:
    await bot.virtualfisher.update_one(
        {"_id": ctx.author.id}, {"$set": {"cooldown": cooldown}}
    )
    await ctx.respond(
        embed=discord.Embed(
            description=f"Cooldown changed to {cooldown} seconds!",
            color=discord.Color.green(),
        )
    )


bot.run(
    os.environ.get("BOTTOKEN"),
    reconnect=True,
)
