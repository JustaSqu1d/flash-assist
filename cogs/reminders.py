import discord
from discord.ext import commands

import asyncio
from main import open_account, Invite
from replit import db
import random

class Reminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_reminder(self, msg):
        try:
            ctx = msg.channel
            msg.content = msg.content.lower()

            if msg.author.id == 878007103460089886:
                try:
                    try:
                        msg2 = await msg.channel.fetch_message(
                            msg.reference.message_id)
                        user = msg2.author
                    except:
                        user = msg.mentions[0]
                except:
                    pass

                try:
                    embed = msg.embeds[0].to_dict()
                    health = embed["title"].split(" ")[1].split("*")[0].split("/")

                    db["enderdragon"]["max"] = health[1]
                    db["enderdragon"]["cur"] = health[0]

                except:
                    pass

                try:
                    await open_account(user)
                except:
                    return

                if not (db[str(user.id)]["mine"] and db[str(user.id)]["fight"]
                        and db[str(user.id)]["chop"] and db[str(user.id)]["ed"]):
                    return

                if "you mined" in msg.content and "in the nether" not in msg.content and db[
                        str(user.id)]["mine"]:
                    if db[str(user.id)]["efficiency"] == 1:
                        cooldown = 4
                    else:
                        cooldown = 5
                    command = "mine"
                elif "you chopped" in msg.content and "in the nether" not in msg.content and db[
                        str(user.id)]["chop"]:
                    command = "chop"
                    if db[str(user.id)]["efficiency"] == 1:
                        cooldown = 45
                    else:
                        cooldown = 60
                elif "you killed" in msg.content and "in the nether" not in msg.content and db[
                        str(user.id)]["fight"]:
                    cooldown = 40
                    command = "fight"
                    if db[str(user.id)]["armor"] == 1:
                        cooldown = 40
                    elif db[str(user.id)]["armor"] == 2:
                        cooldown = 37
                    elif db[str(user.id)]["armor"] == 3:
                        cooldown = 35
                    elif db[str(user.id)]["armor"] == 4:
                        cooldown = 30
                    elif db[str(user.id)]["armor"] == 5:
                        cooldown = 25
                    elif db[str(user.id)]["armor"] == 6:
                        cooldown = 20
                    if db[str(user.id)]["efficiency"] == 1:
                        cooldown -= 10
                elif "you dealt" in msg.content and db[str(user.id)]["ed"]:

                    times = db[str(user.id)]["dragon"]
                    cooldown = 60 * times
                    command = "enderdragon"
                elif "you mined" in msg.content and "in the nether" in msg.content and db[
                        str(user.id)]["mine"]:
                    cooldown = 5
                    command = "nether mine"
                elif "you chopped" in msg.content and "in the nether" in msg.content and db[
                        str(user.id)]["chop"]:
                    cooldown = 60
                    command = "nether chop"
                elif "you killed" in msg.content and "in the nether" in msg.content and db[
                        str(user.id)]["fight"]:
                    cooldown = 45
                    command = "nether fight"
                else:
                    return
                response = db[str(user.id)]["response"]
                try:
                    response = response.replace("%", f"{user.mention}")
                    response = response.replace("&", f"{command}")
                    response = response.replace("$", f"{cooldown}")
                except:
                    pass

                await asyncio.sleep(cooldown)
                await ctx.send(response)
                if random.randint(1, 10) == random.randint(1, 10):
                    view = discord.ui.View()
                    view.add_item(Invite())
                    await ctx.send(response, view=view)
                else:
                    await ctx.send(response)

            if msg.author.id == 625363818968776705:
                try:
                    try:
                        msg2 = await msg.channel.fetch_message(
                            msg.reference.message_id)
                        user = msg2.author
                    except:
                        user = msg.mentions[0]
                except:
                    pass

                try:
                    embed = msg.embeds[0].to_dict()
                    url = embed['author']['icon_url']
                    id = url.split("/")[4]
                    stats = embed['fields'][0][
                        "value"]  #"Mine: 7353\nFight: 755\nChops: 732"
                    stats = stats.split("\n")
                    stats2 = {}

                    for stat in stats:
                        value = stat.split(":")[1]
                        command = (stat.split(":")[0]).lower()
                        stats2[command] = value
                        while 1:
                            try:
                                db[str(id)]["stats"][command] = value
                                break
                            except:
                                db[str(id)]["stats"] = {}
                except:
                    pass

                try:
                    embed = msg.embeds[0].to_dict()
                    id = embed["fields"][1]["value"].split("=")[1].split(")")[0]
                    stats = embed["fields"][2]["value"].split("\n")
                    for stat in stats:
                        value = stat.split(":")[1]
                        command = (stat.split(":")[0]).lower()
                        if command == "mines": command = "mine"
                        if command == "fights": command = "fight"
                        if command == "chops": command = "chops"
                        if command == "total votes": continue
                        while 1:
                            try:
                                db[str(id)]["stats"][command] = value
                                break
                            except:
                                db[str(id)]["stats"] = {}

                except:
                    pass

                try:
                    embed = msg.embeds[0].to_dict()
                    author = embed["author"]["name"].split(" •")[0]
                    member = msg.guild.get_member_named(author)
                    id = member.id

                    db[str(id)]["stats"]["mine"] = embed["fields"][0][
                        "value"].split("\n")[1].split("/")[0]
                    db[str(id)]["stats"]["chops"] = embed["fields"][1][
                        "value"].split("\n")[1].split("/")[0]
                    db[str(id)]["stats"]["fight"] = embed["fields"][2][
                        "value"].split("\n")[1].split("/")[0]

                except:
                    pass

                try:
                    await open_account(user)
                except:
                    return

                if not (db[str(user.id)]["mine2"] and db[str(user.id)]["fight2"]
                        and db[str(user.id)]["chop2"] and db[str(user.id)]["ed2"]):
                    return

                await open_account(user)
                if "you mined" in msg.content:
                    db["trials"] += 1
                    if "boss key" in msg.content:
                        db["success"] += 1
                    if db[str(user.id)]["mine2"]:
                        if db[str(user.id)]["efficiency2"] == 1:
                            cooldown = 4
                        else:
                            cooldown = 5
                        command = "mine"

                elif "you chopped" in msg.content and db[str(user.id)]["chop2"]:
                    if db[str(user.id)]["efficiency2"] == 1:
                        cooldown = 45
                    else:
                        cooldown = 60
                    command = "chop"

                elif "you killed" in msg.content and db[str(user.id)]["fight2"]:
                    if db[str(user.id)]["efficiency2"] == 1:
                        cooldown = 35
                    else:
                        cooldown = 45
                    command = "fight"
                else:
                    return
                response = db[str(user.id)]["response"]

                try:
                    response = response.replace("%", f"{user.mention}")
                except:
                    pass
                try:
                    response = response.replace("&", f"{command}")
                except:
                    pass
                try:
                    response = response.replace("$", f"{cooldown}")
                except:
                    pass
                await asyncio.sleep(cooldown)

                if random.randint(1, 10) == random.randint(1, 10):
                    view = discord.ui.View()
                    view.add_item(Invite())
                    await ctx.send(response, view=view)
                else:
                    await ctx.send(response)

            if msg.author.id == 574652751745777665:
                try:
                    try:
                        msg2 = await msg.channel.fetch_message(
                            msg.reference.message_id)
                        user = msg2.author
                    except:
                        user = msg.interaction.user
                except:
                    pass

                for embed in msg.embeds:
                    embed = embed.to_dict()

                    try:
                        if "You will now find more treasure for the next" in embed[
                                "description"]:
                            minutes = int(embed["description"].split(" ")[10])
                            type = "Treasure"
                            seconds = minutes * 60

                        elif "You will now catch more fish for the next" in embed[
                                "description"]:
                            minutes = int(embed["description"].split(" ")[10])
                            type = "Fish"
                            seconds = minutes * 60

                        elif "You hired a worker for the next" in embed[
                                "description"] and "catches will automatically be added to your inventory.":
                            minutes = int(
                                embed["description"].split(" ")[8].split("**")[1])
                            type = "Worker"
                            seconds = minutes * 60

                        else:
                            continue

                        await asyncio.sleep(seconds)
                        await ctx.send(f"{user.mention} {type} boost has elapsed!")

                    except:
                        pass

        except:
            pass


def setup(bot):
    bot.add_cog(Reminders(bot))