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
    "https://b0f5a63f88654de6beb78898668cc652@o1159308.ingest.sentry.io/6244172",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
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
    try:
        if msg.author.id in bots: bot.dispatch("reminder", msg)
        elif msg.author.id == 586743480651350063 and msg.content == "%reload cogs":
            for filename in os.listdir("cogs"):
                if filename.endswith(".py"):
                    bot.reload_extension(f"cogs.{filename[:-3]}")
            await msg.channel.send("Reload success!")
        else:
            return
    except:
        pass

@bot.event
async def on_interaction(itx):
    await open_account(itx.user)
    await bot.process_application_commands(itx)

@bot.slash_command(
    name="terms",
    description="You can view our Terms of Service and Privacy Policy here.")
async def terms(ctx):
    await ctx.defer()
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
    if "%" not in response:
        failed = discord.Embed(
            title="Missing Arguments!",
            description=
            "Make your own custom reminder with `%response <response>`\nPlease use the following format in your message:\n**Put `%` on where you want you to be mentioned.**\n`&` for the command name.^\n`$` for the command cooldown.^\n\n*^optional*"
        )
        failed.add_field(
            name="Example",
            value=
            f"`%response % hi & cd:$`\nResults in\n\n{ctx.author.mention} hi mine cd:5"
        )
        await ctx.respond(embed=failed)
        return
    user = ctx.author
    db[str(user.id)]["response"] = response
    success = discord.Embed(title="Success!", color=discord.Color.green())
    await ctx.respond(embed=success)


@bot.slash_command(name="invite", description="Invite me to join your server!")
async def invite(ctx):
    embed = discord.Embed(title="Invite me. :)", color=discord.Color.orange())
    embed.description = ""
    view = discord.ui.View()
    view.add_item(Invite())
    view.add_item(Invite2())
    await ctx.respond(embed=embed, view=view)


@bot.slash_command(name="guide", description="Minecord? Whaaa....?")
async def guide(ctx):
    embed = discord.Embed(
        title="Minecord Guide",
        color=discord.Color.orange(),
        url="https://just-a-squid.gitbook.io/minecord-1/v/minecord/")
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
                if not (db[str(user.id)]["mine"]):
                    child.style = discord.ButtonStyle.danger
            if child.label == "Fight":
                if not (db[str(user.id)]["fight"]):
                    child.style = discord.ButtonStyle.danger
            if child.label == "Chop":
                if not (db[str(user.id)]["chop"]):
                    child.style = discord.ButtonStyle.danger
            if child.label == "Enderdragon":
                if not (db[str(user.id)]["ed"]):
                    child.style = discord.ButtonStyle.danger

    @discord.ui.button(label='Mine', style=discord.ButtonStyle.success)
    async def callback(self, button, interaction):
        button.style = discord.ButtonStyle.danger if button.style == discord.ButtonStyle.success else discord.ButtonStyle.success

        db[str(self.ctx.author.id)]["mine"] = not (db[str(
            self.ctx.author.id)]["mine"])
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label='Fight', style=discord.ButtonStyle.success)
    async def callback2(self, button, interaction):
        button.style = discord.ButtonStyle.danger if button.style == discord.ButtonStyle.success else discord.ButtonStyle.success

        db[str(self.ctx.author.id)]["fight"] = not (db[str(
            self.ctx.author.id)]["fight"])
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label='Chop', style=discord.ButtonStyle.success)
    async def callback3(self, button, interaction):
        button.style = discord.ButtonStyle.danger if button.style == discord.ButtonStyle.success else discord.ButtonStyle.success

        db[str(self.ctx.author.id)]["chop"] = not (db[str(
            self.ctx.author.id)]["chop"])
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label='Enderdragon', style=discord.ButtonStyle.success)
    async def callback4(self, button, interaction):
        button.style = discord.ButtonStyle.danger if button.style == discord.ButtonStyle.success else discord.ButtonStyle.success

        db[str(self.ctx.author.id)]["ed"] = not (db[str(
            self.ctx.author.id)]["ed"])
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label='Minecord',
                       style=discord.ButtonStyle.primary,
                       row=2)
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
                if not (db[str(user.id)]["mine2"]):
                    child.style = discord.ButtonStyle.danger
            if child.label == "Fight":
                if not (db[str(user.id)]["fight2"]):
                    child.style = discord.ButtonStyle.danger
            if child.label == "Chop":
                if not (db[str(user.id)]["chop2"]):
                    child.style = discord.ButtonStyle.danger
            if child.label == "Enderdragon":
                if not (db[str(user.id)]["ed2"]):
                    child.style = discord.ButtonStyle.danger

    @discord.ui.button(label='Mine', style=discord.ButtonStyle.success)
    async def callback(self, button, interaction):
        button.style = discord.ButtonStyle.danger if button.style == discord.ButtonStyle.success else discord.ButtonStyle.success

        db[str(self.ctx.author.id)]["mine2"] = not (db[str(
            self.ctx.author.id)]["mine2"])
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label='Fight', style=discord.ButtonStyle.success)
    async def callback2(self, button, interaction):
        button.style = discord.ButtonStyle.danger if button.style == discord.ButtonStyle.success else discord.ButtonStyle.success

        db[str(self.ctx.author.id)]["fight2"] = not (db[str(
            self.ctx.author.id)]["fight2"])
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label='Chop', style=discord.ButtonStyle.success)
    async def callback3(self, button, interaction):
        button.style = discord.ButtonStyle.danger if button.style == discord.ButtonStyle.success else discord.ButtonStyle.success

        db[str(self.ctx.author.id)]["chop2"] = not (db[str(
            self.ctx.author.id)]["chop2"])
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label='Enderdragon', style=discord.ButtonStyle.success)
    async def callback4(self, button, interaction):
        button.style = discord.ButtonStyle.danger if button.style == discord.ButtonStyle.success else discord.ButtonStyle.success

        db[str(self.ctx.author.id)]["ed2"] = not (db[str(
            self.ctx.author.id)]["ed2"])
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label='Minecord Classic',
                       style=discord.ButtonStyle.primary,
                       row=2)
    async def callback5(self, button, interaction):
        self.value = False
        self.stop()


keep_alive()
bot.run(os.environ['BOTTOKEN'])
