import discord
from discord.ext import tasks
from discord.commands import Option
import os 
from keepalive import keep_alive
import asyncio
from replit import db
import random
import aiohttp

bots = [878007103460089886, 625363818968776705, 574652751745777665]

async def changedatabase():
  async with aiohttp.botSession() as session:
    async with session.get(f"https://VMA.squidsquidsquid.repl.co/{os.environ['PW']}") as response:
      html = await response.text()
      db.db_url = str(html)

class Invite(discord.ui.Button):
  def __init__(self):
    super().__init__(label='Invite me!', style=discord.ButtonStyle.link,
                      url="https://discord.com/oauth2/authorize?bot_id=836581672811495465&permissions=321536&scope=bot%20applications.commands", row = 1)

class Invite2(discord.ui.Button):
  def __init__(self):
    super().__init__(label='Alternative link.', style=discord.ButtonStyle.link,
                      url="https://discord.com/oauth2/authorize?bot_id=931981494887534602&permissions=321536&scope=bot%20applications.commands", row = 1)

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = discord.AutoShardedBot(intents=intents, activity=discord.Game(name="Discord Bots | /setup"))
bot.load_extension('cogs.verify')
bot.load_extension('cogs.ender_listen')
bot.load_extension('cogs.vf_verify')

class Option1(discord.ui.View):
    def __init__(self):
      super().__init__(timeout=60)
      self.value = None

    @discord.ui.button(label='Minecord' , style=discord.ButtonStyle.primary)
    async def callback(self, button, interaction):
      self.value = False
      self.stop()
      
    @discord.ui.button(label='Minecord Classic' , style=discord.ButtonStyle.secondary)
    async def callback2(self, button, interaction):
      self.value = True
      self.stop()

class Option2(discord.ui.View):
    def __init__(self):
      super().__init__(timeout=60)
      self.value = None

    @discord.ui.button(label='Yes' , style=discord.ButtonStyle.success)
    async def callback(self, button, interaction):
      self.value = True
      self.stop()
      
    @discord.ui.button(label='No' , style=discord.ButtonStyle.danger)
    async def callback2(self, button, interaction):
      self.value = False
      self.stop()

class OptionAr(discord.ui.View):
    def __init__(self):
      super().__init__(timeout=60)
      self.value = None

    @discord.ui.button(label='Chainmail Armor' , style=discord.ButtonStyle.danger)
    async def callback(self, button, interaction):
      self.value = 2
      self.stop()
      
    @discord.ui.button(label='Iron Armor' , style=discord.ButtonStyle.primary)
    async def callback2(self, button, interaction):
      self.value = 3
      self.stop()
    
    @discord.ui.button(label='Gold Armor' , style=discord.ButtonStyle.success)
    async def callback3(self, button, interaction):
      self.value = 4
      self.stop()
    
    @discord.ui.button(label='Diamond Armor' , style=discord.ButtonStyle.secondary)
    async def callback4(self, button, interaction):
      self.value = 5
      self.stop()
    
    @discord.ui.button(label='Netherite Armor' , style=discord.ButtonStyle.secondary)
    async def callback5(self, button, interaction):
      self.value = 6
      self.stop()

class OptionMin(discord.ui.View):
    def __init__(self):
      super().__init__(timeout=60)
      self.value = None

    @discord.ui.button(label='1' , style=discord.ButtonStyle.danger)
    async def callback(self, button, interaction):
      self.value = 1
      self.stop()
      
    @discord.ui.button(label='2' , style=discord.ButtonStyle.primary)
    async def callback2(self, button, interaction):
      self.value = 2
      self.stop()
    
    @discord.ui.button(label='3' , style=discord.ButtonStyle.primary)
    async def callback3(self, button, interaction):
      self.value = 3
      self.stop()
    
    @discord.ui.button(label='4' , style=discord.ButtonStyle.success)
    async def callback4(self, button, interaction):
      self.value = 4
      self.stop()
    
    @discord.ui.button(label='5' , style=discord.ButtonStyle.success)
    async def callback5(self, button, interaction):
      self.value = 5

@tasks.loop(seconds=10.0)
async def update_url():
  await changedatabase()

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

    db[str(user.id)]["response"] = "% Time to &! `m!&`\nCurrent cooldown is `$ seconds`!"

  return True

@bot.event
async def on_ready():
  print("Logged in as {0.user}".format(bot))
  update_url.start()
  print(f"{len(bot.guilds)} servers")

@bot.event
async def on_message(msg):
  try:
    if msg.author.id in bots: bot.dispatch("reminder", msg)
  except:
    pass
    
@bot.event
async def on_reminder(msg):
  try:
    ctx = msg.channel
    msg.content = msg.content.lower()
    
    if msg.author.id == 878007103460089886:
      try:
        try:
          msg2 = await msg.channel.fetch_message(msg.reference.message_id)
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
      
      if not(db[str(user.id)]["mine"] and db[str(user.id)]["fight"] and db[str(user.id)]["chop"] and db[str(user.id)]["ed"]): return
      
      if "you mined" in msg.content and "in the nether" not in msg.content and db[str(user.id)]["mine"]:
        if db[str(user.id)]["efficiency"] == 1:
          cooldown = 4
        else:
          cooldown = 5
        command = "mine"
      elif "you chopped" in msg.content and "in the nether" not in msg.content and db[str(user.id)]["chop"]:
        command = "chop"
        if db[str(user.id)]["efficiency"] == 1:
          cooldown = 45
        else:
          cooldown = 60
      elif "you killed" in msg.content and "in the nether" not in msg.content and db[str(user.id)]["fight"]:
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
        cooldown = 60*times
        command = "enderdragon"
      elif "you mined" in msg.content and "in the nether" in msg.content and db[str(user.id)]["mine"]:
        cooldown = 5
        command = "nether mine"
      elif "you chopped" in msg.content and "in the nether" in msg.content and db[str(user.id)]["chop"]:
        cooldown = 60
        command = "nether chop"
      elif "you killed" in msg.content and "in the nether" in msg.content and db[str(user.id)]["fight"]:
        cooldown = 45
        command = "nether fight"
      else:
        return
      response = db[str(user.id)]["response"]
      try:
        response = response.replace("%",f"{user.mention}")
        response = response.replace("&",f"{command}")
        response = response.replace("$",f"{cooldown}")
      except:
        pass
      
      await asyncio.sleep(cooldown)
      await ctx.send(response)
      if random.randint(1,10) == random.randint(1,10):
        view = discord.ui.View()
        view.add_item(Invite())
        await ctx.send(response, view = view)
      else:
        await ctx.send(response)
  
    if msg.author.id == 625363818968776705:
      try:
        try:
          msg2 = await msg.channel.fetch_message(msg.reference.message_id)
          user = msg2.author
        except:
          user = msg.mentions[0]
      except:
        pass
      
      try:
          embed = msg.embeds[0].to_dict()
          url = embed['author']['icon_url']
          id = url.split("/")[4]
          stats = embed['fields'][0]["value"] #"Mine: 7353\nFight: 755\nChops: 732"
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
        
        db[str(id)]["stats"]["mine"] = embed["fields"][0]["value"].split("\n")[1].split("/")[0]
        db[str(id)]["stats"]["chops"] = embed["fields"][1]["value"].split("\n")[1].split("/")[0]
        db[str(id)]["stats"]["fight"] = embed["fields"][2]["value"].split("\n")[1].split("/")[0]
  
      except:
        pass
  
      try:
        await open_account(user)
      except:
        return
      
      if not(db[str(user.id)]["mine2"] and db[str(user.id)]["fight2"] and db[str(user.id)]["chop2"] and db[str(user.id)]["ed2"]): return
  
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
        response = response.replace("%",f"{user.mention}")
      except:
        pass
      try:
        response = response.replace("&",f"{command}")
      except:
        pass
      try:
        response = response.replace("$",f"{cooldown}")
      except:
        pass
      await asyncio.sleep(cooldown)
      
      if random.randint(1,10) == random.randint(1,10):
        view = discord.ui.View()
        view.add_item(Invite())
        await ctx.send(response, view = view)
      else:
        await ctx.send(response)
        
    if msg.author.id == 574652751745777665:
      try:
        try:
          msg2 = await msg.channel.fetch_message(msg.reference.message_id)
          user = msg2.author
        except:
          user = msg.interaction.user
      except:
        pass
      
      for embed in msg.embeds:
        embed = embed.to_dict()
        print(f"{embed}\n")
        
        try:
          if "You will now find more treasure for the next" in embed["description"]:
            minutes = int(embed["description"].split(" ")[10])
            type = "Treasure"
            seconds = minutes*60

  
          elif "You will now catch more fish for the next" in embed["description"]:
            minutes = int(embed["description"].split(" ")[10])
            type = "Fish"
            seconds = minutes*60
  

          elif "You hired a worker for the next" in embed["description"] and "catches will automatically be added to your inventory.":
            minutes = int(embed["description"].split(" ")[8].split("**")[1])
            type = "Worker"
            seconds = minutes*60

          else:
            continue

          await asyncio.sleep(seconds)
          await ctx.send(f"{user.mention} {type} boost has elapsed!")
        
        except:
          pass
          
  except:
    pass
    
@bot.event
async def on_interaction(itx):
  await open_account(itx.user)
  await bot.process_application_commands(itx)

@bot.slash_command(name="terms", description="You can view our Terms of Service and Privacy Policy here.")
async def terms(ctx):
  await ctx.defer()
  embed = discord.Embed(title="Flash Assist Terms")
  embed.add_field(name="Links", value="[Terms of Service](https://flash-assist.squidsquidsquid.repl.co/terms)\n[Privacy Policy](https://flash-assist.squidsquidsquid.repl.co/privacy-policy)", inline = False)
  await ctx.followup.send(embed=embed)

@bot.slash_command(name="setup", description="Change your settings!")
async def setup(ctx):
  await ctx.defer(ephemeral=True)
  await open_account(ctx.author)
  user = ctx.author
  view = Option1()
  em = discord.Embed(title = "What are your settings for?", color = ctx.author.color)
  em.set_footer(text = f"© just a squid#5483 2022 | m!help | {ctx.author}")
  await ctx.followup.send(embed = em, view = view)
  
  timedout = await view.wait()

  if timedout:
    for child in view.children:
        child.disabled = True
    await ctx.interaction.edit_original_message(view=view)
    return

  if view.value:

    em = discord.Embed(title = "Do you have efficiency?", description = "Yes | No", color = ctx.author.color)
    em.set_footer(text = f"© just a squid#5483 2022 | m!help | {ctx.author}")
    op1 = Option2()
    await ctx.interaction.edit_original_message(embed = em, view = op1)

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

    em = discord.Embed(title = "What armor do you have?", color = ctx.author.color)

    em.set_footer(text = f"© just a squid#5483 2022 | %setup | {ctx.author}")
    await ctx.interaction.edit_original_message(embed = em, view = opar)

    timedout = await opar.wait()

    if timedout:
      for child in opar.children:
          child.disabled = True
      await ctx.interaction.edit_original_message(view=opar)
      return

    db[str(user.id)]["armor"] = opar.value

    em = discord.Embed(title = "What is your Ender Dragon cooldown (answer in minutes)?", description = "Enter a number!", color = ctx.author.color)
    em.set_footer(text = f"© just a squid#5483 2022 | m!help | {ctx.author}")

    opmin = OptionMin()

    await ctx.interaction.edit_original_message(embed = em, view = opmin)
    
    timedout = await opmin.wait()

    if timedout:
      for child in opmin.children:
          child.disabled = True
      await ctx.interaction.edit_original_message(view=opmin)
      return

    db[str(user.id)]["armor"] = opmin.value

    em = discord.Embed(title = "Setup Complete!", color = discord.Color.green())
    em.set_footer(text = f"© just a squid#5483 2022 | m!help | {ctx.author}")

    for child in opmin.children:
      child.disabled = True
    await ctx.interaction.edit_original_message(view=opmin)

    await ctx.interaction.edit_original_message(embed = em, view = opmin)
    return

  else:
    em = discord.Embed(title = "Do you have efficiency?", description = "Yes | No", color = ctx.author.color)
    em.set_footer(text = f"© just a squid#5483 2022 | m!help | {ctx.author}")
    
    op1 = Option2()
    await ctx.interaction.edit_original_message(embed = em, view = op1)

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
    
    em = discord.Embed(title = "Setup Complete!", color = discord.Color.green())
    em.set_footer(text = f"© just a squid#5483 2022 | m!help | {ctx.author}")

    for child in op1.children:
      child.disabled = True

    await ctx.interaction.edit_original_message(embed = em, view = op1)
    return

@bot.slash_command(name="config", description="Edit what commands you want to be reminded upon!!")
async def config(ctx):

  embed = discord.Embed(title="Reminder Control Panel!",description="Green: ON\nRed: OFF")
  view = Toggles(ctx)
  await ctx.respond(embed=embed, view = view, ephemeral=True)
  to = await view.wait()
  while not(to):
    if not(view.value):
      view = TogglesCl(ctx)
      await ctx.interaction.edit_original_message(view = view)
    else:
      view = Toggles(ctx)
      await ctx.interaction.edit_original_message(view = view)
    to = await view.wait()

@bot.slash_command(name= "droprate", description="Find the drop-rate of boss keys!")
async def droprate(ctx):
    embed = discord.Embed(title="Boss Key Drop Rates", color =discord.Color.orange())
    embed.add_field(name="Boss Key Drops",value=db["success"],inline=False)
    embed.add_field(name="Mines Recorded",value=db["trials"],inline=False)
    embed.set_footer(text=f'Estimated chance of Boss Key drop: {round((db["success"]/db["trials"]*100))}%')
    await ctx.respond(embed = embed)

@bot.slash_command(name= "response", description="Use your own custom reminder messages!")
async def _response(ctx, 
  response: Option(str, description="Use custom response messages!", required=True)
):
  if "%" not in response:
    failed = discord.Embed(title="Missing Arguments!",description="Make your own custom reminder with `%response <response>`\nPlease use the following format in your message:\n**Put `%` on where you want you to be mentioned.**\n`&` for the command name.^\n`$` for the command cooldown.^\n\n*^optional*")
    failed.add_field(name="Example",value=f"`%response % hi & cd:$`\nResults in\n\n{ctx.author.mention} hi mine cd:5")
    await ctx.respond(embed=failed)
    return
  user = ctx.author
  db[str(user.id)]["response"] = response
  success = discord.Embed(title="Success!",color=discord.Color.green())
  await ctx.respond(embed = success)

@bot.slash_command(name= "invite", description="Invite me to join your server!")
async def invite(ctx):
  embed = discord.Embed(title="Invite me. :)",color=discord.Color.orange())
  embed.description = ""
  view = discord.ui.View()
  view.add_item(Invite())
  view.add_item(Invite2())
  await ctx.respond(embed=embed, view=view)
  
@bot.slash_command(name= "guide", description="Minecord? Whaaa....?")
async def guide(ctx):
  embed = discord.Embed(title="Minecord Guide",color=discord.Color.orange(),url="https://just-a-squid.gitbook.io/minecord-1/v/minecord/")
  await ctx.respond(embed=embed)

class TogglesCl(discord.ui.View):
    def __init__(self, ctx):
      super().__init__(timeout=60)
      self.value = None
      self.ctx = ctx
      #[<Button style=<ButtonStyle.success: 3> url=None disabled=False label='Mine' emoji=None row=None>, <Button style=<ButtonStyle.success: 3> url=None disabled=False label='Fight' emoji=None row=None>, <Button style=<ButtonStyle.success: 3> url=None disabled=False label='Chop' emoji=None row=None>, <Button style=<ButtonStyle.success: 3> url=None disabled=False label='Enderdragon' emoji=None row=None>, <Button style=<ButtonStyle.primary: 1> url=None disabled=False label='Minecord Classic' emoji=None row=2>]
      user = self.ctx.author
      for child in self.children:
        if child.label == "Mine":
          if not(db[str(user.id)]["mine"]):
            child.style = discord.ButtonStyle.danger
        if child.label == "Fight":
          if not(db[str(user.id)]["fight"]):
            child.style = discord.ButtonStyle.danger
        if child.label == "Chop":
          if not(db[str(user.id)]["chop"]):
            child.style = discord.ButtonStyle.danger
        if child.label == "Enderdragon":
          if not(db[str(user.id)]["ed"]):
            child.style = discord.ButtonStyle.danger

    @discord.ui.button(label='Mine' , style=discord.ButtonStyle.success)
    async def callback(self, button, interaction):
      button.style = discord.ButtonStyle.danger if button.style == discord.ButtonStyle.success else discord.ButtonStyle.success

      db[str(self.ctx.author.id)]["mine"] = not(db[str(self.ctx.author.id)]["mine"])
      await interaction.response.edit_message(view=self)
      
    @discord.ui.button(label='Fight' , style=discord.ButtonStyle.success)
    async def callback2(self, button, interaction):
      button.style = discord.ButtonStyle.danger if button.style == discord.ButtonStyle.success else discord.ButtonStyle.success

      db[str(self.ctx.author.id)]["fight"] = not(db[str(self.ctx.author.id)]["fight"])
      await interaction.response.edit_message(view=self)
    
    @discord.ui.button(label='Chop' , style=discord.ButtonStyle.success)
    async def callback3(self, button, interaction):
      button.style = discord.ButtonStyle.danger if button.style == discord.ButtonStyle.success else discord.ButtonStyle.success

      db[str(self.ctx.author.id)]["chop"] = not(db[str(self.ctx.author.id)]["chop"])
      await interaction.response.edit_message(view=self)
    
    @discord.ui.button(label='Enderdragon' , style=discord.ButtonStyle.success)
    async def callback4(self, button, interaction):
      button.style = discord.ButtonStyle.danger if button.style == discord.ButtonStyle.success else discord.ButtonStyle.success

      db[str(self.ctx.author.id)]["ed"] = not(db[str(self.ctx.author.id)]["ed"])
      await interaction.response.edit_message(view=self)
    
    @discord.ui.button(label='Minecord' , style=discord.ButtonStyle.primary, row=2)
    async def callback5(self, button, interaction):
      self.value = True
      self.stop()

class Toggles(discord.ui.View):
    def __init__(self, ctx):
      super().__init__(timeout=60)
      self.value = None
      self.ctx = ctx
      #[<Button style=<ButtonStyle.success: 3> url=None disabled=False label='Mine' emoji=None row=None>, <Button style=<ButtonStyle.success: 3> url=None disabled=False label='Fight' emoji=None row=None>, <Button style=<ButtonStyle.success: 3> url=None disabled=False label='Chop' emoji=None row=None>, <Button style=<ButtonStyle.success: 3> url=None disabled=False label='Enderdragon' emoji=None row=None>, <Button style=<ButtonStyle.primary: 1> url=None disabled=False label='Minecord Classic' emoji=None row=2>]
      user = self.ctx.author
      for child in self.children:
        if child.label == "Mine":
          if not(db[str(user.id)]["mine2"]):
            child.style = discord.ButtonStyle.danger
        if child.label == "Fight":
          if not(db[str(user.id)]["fight2"]):
            child.style = discord.ButtonStyle.danger
        if child.label == "Chop":
          if not(db[str(user.id)]["chop2"]):
            child.style = discord.ButtonStyle.danger
        if child.label == "Enderdragon":
          if not(db[str(user.id)]["ed2"]):
            child.style = discord.ButtonStyle.danger

    @discord.ui.button(label='Mine' , style=discord.ButtonStyle.success)
    async def callback(self, button, interaction):
      button.style = discord.ButtonStyle.danger if button.style == discord.ButtonStyle.success else discord.ButtonStyle.success

      db[str(self.ctx.author.id)]["mine2"] = not(db[str(self.ctx.author.id)]["mine2"])
      await interaction.response.edit_message(view=self)
      
    @discord.ui.button(label='Fight' , style=discord.ButtonStyle.success)
    async def callback2(self, button, interaction):
      button.style = discord.ButtonStyle.danger if button.style == discord.ButtonStyle.success else discord.ButtonStyle.success

      db[str(self.ctx.author.id)]["fight2"] = not(db[str(self.ctx.author.id)]["fight2"])
      await interaction.response.edit_message(view=self)
    
    @discord.ui.button(label='Chop' , style=discord.ButtonStyle.success)
    async def callback3(self, button, interaction):
      button.style = discord.ButtonStyle.danger if button.style == discord.ButtonStyle.success else discord.ButtonStyle.success

      db[str(self.ctx.author.id)]["chop2"] = not(db[str(self.ctx.author.id)]["chop2"])
      await interaction.response.edit_message(view=self)
    
    @discord.ui.button(label='Enderdragon' , style=discord.ButtonStyle.success)
    async def callback4(self, button, interaction):
      button.style = discord.ButtonStyle.danger if button.style == discord.ButtonStyle.success else discord.ButtonStyle.success

      db[str(self.ctx.author.id)]["ed2"] = not(db[str(self.ctx.author.id)]["ed2"])
      await interaction.response.edit_message(view=self)
    
    @discord.ui.button(label='Minecord Classic' , style=discord.ButtonStyle.primary, row=2)
    async def callback5(self, button, interaction):
      self.value = False
      self.stop()


keep_alive()
bot.run(os.environ['BOTTOKEN'])