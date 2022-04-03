from replit import db
import os
import discord
import asyncio
import random
from views import Vote
import traceback

api_key = os.environ['SPKEY']
page_id = 'm4j4kdx61gkt'
metric_id = 'btv9x2yn5b90'
api_base = 'api.statuspage.io/v1'        

in_progress = 0

async def open_account(user):

    if str(user.id) in db:
        return False

    else:
        db[str(user.id)] = {}
        db[str(user.id)]["efficiency"] = 0
        db[str(user.id)]["armor"] = 0
        db[str(user.id)]["dragon"] = 5
        db[str(user.id)]["mine"] = True
        db[str(user.id)]["fight"] = True
        db[str(user.id)]["chop"] = True
        db[str(user.id)]["ed"] = True

        db[str(user.id)]["efficiency2"] = 0
        db[str(user.id)]["mine2"] = True
        db[str(user.id)]["fight2"] = True
        db[str(user.id)]["chop2"] = True
        db[str(user.id)]["ed2"] = True

        db[str(user.id)]["treasure"] = True
        db[str(user.id)]["fish"] = True
        db[str(user.id)]["worker"] = True
        db[str(user.id)]["vfdaily"] = True
        
        db[str(
            user.id
        )]["response"] = "% & boost/command cooldown elapsed! \nCurrent cooldown is `$ seconds`!"

    return True

async def reminder(msg : discord.Message):
    
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
                return

            
            try:
                await open_account(user)
            except:
                return


            if not (db[str(user.id)]["mine"] or db[str(user.id)]["fight"]
                    or db[str(user.id)]["chop"] or db[str(user.id)]["ed"]):
                return

            if "youmined" in msg.content and "inthenether" not in msg.content and db[
                    str(user.id)]["mine"]:
                if db[str(user.id)]["efficiency"] == 1:
                    cooldown = 4
                else:
                    cooldown = 5
                command = "mine"
            elif "you chopped" in msg.content and "inthenether" not in msg.content and db[
                    str(user.id)]["chop"]:
                command = "chop"
                if db[str(user.id)]["efficiency"] == 1:
                    cooldown = 45
                else:
                    cooldown = 60
            elif "youkilled" in msg.content and "inthenether" not in msg.content and db[
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
            elif "youdealt" in msg.content and db[str(user.id)]["ed"]:
                times = db[str(user.id)]["dragon"]
                cooldown = 60 * times
                command = "enderdragon"
            elif "youmined" in msg.content and "inthenether" in msg.content and db[
                    str(user.id)]["mine"]:
                cooldown = 5
                command = "nether mine"
            elif "youchopped" in msg.content and "inthenether" in msg.content and db[
                    str(user.id)]["chop"]:
                cooldown = 60
                command = "nether chop"
            elif "youkilled" in msg.content and "inthenether" in msg.content and db[
                    str(user.id)]["fight"]: 
                cooldown = 45
                command = "nether fight"
            else:
                return

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

            if not (db[str(user.id)]["mine2"] or db[str(user.id)]["fight2"]
                    or db[str(user.id)]["chop2"] or db[str(user.id)]["ed2"]):
                return

            if "youmined" in msg.content:
                db["trials"] += 1
                if "bosskey" in msg.content:
                    db["success"] += 1
                if db[str(user.id)]["mine2"]:
                    if db[str(user.id)]["efficiency2"] == 1:
                        cooldown = 4
                    else:
                        cooldown = 5
                    command = "mine"

            elif "youchopped" in msg.content and db[str(user.id)]["chop2"]:
                if db[str(user.id)]["efficiency2"] == 1:
                    cooldown = 45
                else:
                    cooldown = 60
                command = "chop"

            elif "youkilled" in msg.content and db[str(user.id)]["fight2"]:
                if db[str(user.id)]["efficiency2"] == 1:
                    cooldown = 35
                else:
                    cooldown = 45
                command = "fight"
            else:
                return

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
            
            
            try:
                db[str(user.id)]["treasure"]
                db[str(user.id)]["fish"]
                db[str(user.id)]["worker"]
            except:
                await open_account(user)
                
                db[str(user.id)]["treasure"] = True
                db[str(user.id)]["fish"] = True
                db[str(user.id)]["worker"] = True
                db[str(user.id)]["vfdaily"] = True


            for embed in msg.embeds:
                embed = embed.to_dict()

                try:
                    if "You will now find more treasure for the next" in embed[
                            "description"] and db[str(user.id)]["treasure"]:
                        minutes = int(embed["description"].split(" ")[10])
                        command = "treasure"
                        cooldown = minutes * 60
                        break

                    elif "You will now catch more fish for the next" in embed[
                            "description"] and db[str(user.id)]["fish"] :
                        minutes = int(embed["description"].split(" ")[10])
                        command = "fish"
                        cooldown = minutes * 60
                        break

                    elif "You hired a worker for the next" in embed[
                            "description"] and "catches will automatically be added to your inventory." and db[str(user.id)]["worker"] :
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
            

        response = db[str(user.id)]["response"]
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
        await asyncio.sleep(cooldown)

        view = discord.ui.View()
        
        if random.randint(1, 10) == random.randint(1, 10):
            view.add_item(Vote())
            
        await ctx.send(response, view=view)

    except UnboundLocalError:
        pass
    
    except discord.errors.Forbidden:
        pass