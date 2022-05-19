import discord
from helpers import fetch_user
from discord.ui import Modal, InputText

class Invite(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Invite me!',
            style=discord.ButtonStyle.link,
            url=
            "https://discord.com/api/oauth2/authorize?client_id=836581672811495465&permissions=0&redirect_uri=https%3A%2F%2Fflash-assist.glitch.me%2F&response_type=code&scope=identify%20bot%20applications.commands",
            row=1)

class Invite2(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Alternative link',
            style=discord.ButtonStyle.link,
            url=
            "https://discord.com/api/oauth2/authorize?client_id=836581672811495465&permissions=321536&redirect_uri=https%3A%2F%2Fdiscord.com%2Finvite%2FfJt6yFeD5v&response_type=code&scope=identify%20bot%20applications.commands",
            row=1)

class Invite3(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Website',
            style=discord.ButtonStyle.link,
            url=
            "https://flash-assist.glitch.me/",
            row=1)

class Invite4(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Discord Server',
            style=discord.ButtonStyle.link,
            url=
            "https://discord.com/invite/fJt6yFeD5v",
            row=2)

class Status(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Bot Status',
            style=discord.ButtonStyle.link,
            url=
            "https://flashassist.statuspage.io/",
            row=2)

class Vote(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Vote for me!',
            style=discord.ButtonStyle.link,
            url=
            "https://top.gg/bot/836581672811495465/vote",
            row=2)

class Option1(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.value = None

    @discord.ui.button(label='Minecord', style=discord.ButtonStyle.primary)
    async def callback(self, button, interaction):
        self.value = False
        self.stop()

    @discord.ui.button(label='Minecord Classic',
                       style=discord.ButtonStyle.secondary)
    async def callback2(self, button, interaction):
        self.value = True
        self.stop()


class Option2(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.value = None

    @discord.ui.button(label='Yes', style=discord.ButtonStyle.success)
    async def callback(self, button, interaction):
        self.value = True
        self.stop()

    @discord.ui.button(label='No', style=discord.ButtonStyle.danger)
    async def callback2(self, button, interaction):
        self.value = False
        self.stop()

class OptionAr(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.value = None

    @discord.ui.button(label='Chainmail Armor',
                       style=discord.ButtonStyle.danger)
    async def callback(self, button, interaction):
        self.value = 2
        self.stop()

    @discord.ui.button(label='Iron Armor', style=discord.ButtonStyle.primary)
    async def callback2(self, button, interaction):
        self.value = 3
        self.stop()

    @discord.ui.button(label='Gold Armor', style=discord.ButtonStyle.success)
    async def callback3(self, button, interaction):
        self.value = 4
        self.stop()

    @discord.ui.button(label='Diamond Armor',
                       style=discord.ButtonStyle.secondary)
    async def callback4(self, button, interaction):
        self.value = 5
        self.stop()

    @discord.ui.button(label='Netherite Armor',
                       style=discord.ButtonStyle.secondary)
    async def callback5(self, button, interaction):
        self.value = 6
        self.stop()


class OptionMin(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.value = None

    @discord.ui.button(label='1', style=discord.ButtonStyle.danger)
    async def callback(self, button, interaction):
        self.value = 1
        self.stop()

    @discord.ui.button(label='2', style=discord.ButtonStyle.primary)
    async def callback2(self, button, interaction):
        self.value = 2
        self.stop()

    @discord.ui.button(label='3', style=discord.ButtonStyle.primary)
    async def callback3(self, button, interaction):
        self.value = 3
        self.stop()

    @discord.ui.button(label='4', style=discord.ButtonStyle.success)
    async def callback4(self, button, interaction):
        self.value = 4
        self.stop()

    @discord.ui.button(label='5', style=discord.ButtonStyle.success)
    async def callback5(self, button, interaction):
        self.value = 5
        self.stop()


class TogglesCl(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.value = None
        self.ctx = ctx
        user = self.ctx.author
        self.db = fetch_user(self.ctx.author, self.ctx.bot)
        for child in self.children:
            try:
                if child.label == "Mine":
                    if not (self.db["minecordclassic"]["mine"]):
                        child.style = discord.ButtonStyle.danger
                if child.label == "Fight":
                    if not (self.db["minecordclassic"]["fight"]):
                        child.style = discord.ButtonStyle.danger
                if child.label == "Chop":
                    if not (self.db["minecordclassic"]["chop"]):
                        child.style = discord.ButtonStyle.danger
                if child.label == "Enderdragon":
                    if not (self.db["minecordclassic"]["ed"]):
                        child.style = discord.ButtonStyle.danger
            except:
                pass

    @discord.ui.button(label='Mine', style=discord.ButtonStyle.success)
    async def callback(self, button, interaction):
        button.style = discord.ButtonStyle.danger if button.style == discord.ButtonStyle.success else discord.ButtonStyle.success

        self.ctx.bot.minecordclassic.update_one({"_id":self.ctx.author.id}, {"$set": {"mine": not (self.db["minecordclassic"]["mine"])}})
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label='Fight', style=discord.ButtonStyle.success)
    async def callback2(self, button, interaction):
        button.style = discord.ButtonStyle.danger if button.style == discord.ButtonStyle.success else discord.ButtonStyle.success

        self.ctx.bot.minecordclassic.update_one({"_id":self.ctx.author.id}, {"$set": {"fight": not (self.db["minecordclassic"]["fight"])}})
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label='Chop', style=discord.ButtonStyle.success)
    async def callback3(self, button, interaction):
        button.style = discord.ButtonStyle.danger if button.style == discord.ButtonStyle.success else discord.ButtonStyle.success

        self.ctx.bot.minecordclassic.update_one({"_id":self.ctx.author.id}, {"$set": {"chop": not (self.db["minecordclassic"]["chop"])}})
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label='Enderdragon', style=discord.ButtonStyle.success)
    async def callback4(self, button, interaction):
        button.style = discord.ButtonStyle.danger if button.style == discord.ButtonStyle.success else discord.ButtonStyle.success

        self.ctx.bot.minecordclassic.update_one({"_id":self.ctx.author.id}, {"$set": {"ed": not (self.db["minecordclassic"]["ed"])}})
        await interaction.response.edit_message(view=self)

    @discord.ui.select(placeholder='Currently editing: Minecord Classic', min_values=1, max_values=1, options=[
        discord.SelectOption(label='Virtual Fisher', description='Edit Virtual Fisher Settings'),
        discord.SelectOption(label='Minecord', description='Edit Minecord Classic Settings')
    ])
    async def select_callback(self, select, interaction):
        self.value = select.values[0]
        self.stop()


class Toggles(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.value = None
        self.ctx = ctx
        self.db = fetch_user(self.ctx.author, self.ctx.bot)
        for child in self.children:
            try:
                if child.label == "Mine":
                    if not (self.db["minecord"]["mine"]):
                        child.style = discord.ButtonStyle.danger
                if child.label == "Fight":
                    if not (self.db["minecord"]["fight"]):
                        child.style = discord.ButtonStyle.danger
                if child.label == "Chop":
                    if not (self.db["minecord"]["chop"]):
                        child.style = discord.ButtonStyle.danger
                if child.label == "Enderdragon":
                    if not (self.db["minecord"]["ed"]):
                        child.style = discord.ButtonStyle.danger
            except:
                pass

    @discord.ui.button(label='Mine', style=discord.ButtonStyle.success)
    async def callback(self, button, interaction):
        button.style = discord.ButtonStyle.danger if button.style == discord.ButtonStyle.success else discord.ButtonStyle.success

        self.ctx.bot.minecord.update_one({"_id":self.ctx.author.id}, {"$set": {"mine": not (self.db["minecord"]["mine"])}})
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label='Fight', style=discord.ButtonStyle.success)
    async def callback2(self, button, interaction):
        button.style = discord.ButtonStyle.danger if button.style == discord.ButtonStyle.success else discord.ButtonStyle.success

        self.ctx.bot.minecord.update_one({"_id":self.ctx.author.id}, {"$set": {"fight": not (self.db["minecord"]["fight"])}})
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label='Chop', style=discord.ButtonStyle.success)
    async def callback3(self, button, interaction):
        button.style = discord.ButtonStyle.danger if button.style == discord.ButtonStyle.success else discord.ButtonStyle.success

        self.ctx.bot.minecord.update_one({"_id":self.ctx.author.id}, {"$set": {"chop": not (self.db["minecord"]["chop"])}})
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label='Enderdragon', style=discord.ButtonStyle.success)
    async def callback4(self, button, interaction):
        button.style = discord.ButtonStyle.danger if button.style == discord.ButtonStyle.success else discord.ButtonStyle.success

        self.ctx.bot.minecord.update_one({"_id":self.ctx.author.id}, {"$set": {"ed": not (self.db["minecord"]["ed"])}})
        await interaction.response.edit_message(view=self)

    @discord.ui.select(placeholder='Currently editing: Minecord', min_values=1, max_values=1, options=[
        discord.SelectOption(label='Virtual Fisher', description='Edit Virtual Fisher Settings'),
        discord.SelectOption(label='Minecord Classic', description='Edit Minecord Classic Settings')
    ])
    async def select_callback(self, select, interaction):
        self.value = select.values[0]
        self.stop()

class TogglesVf(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.value = None
        self.ctx = ctx
        self.db = fetch_user(self.ctx.author, self.ctx.bot)
        for child in self.children:
            try:
                if child.label == "Treasure":
                    if not (self.db["virtualfisher"]["treasure"]):
                        child.style = discord.ButtonStyle.danger
                if child.label == "Fish":
                    if not (self.db["virtualfisher"]["fish"]):
                        child.style = discord.ButtonStyle.danger
                if child.label == "Worker":
                    if not (self.db["virtualfisher"]["worker"]):
                        child.style = discord.ButtonStyle.danger
            except:
                pass

    @discord.ui.button(label='Treasure', style=discord.ButtonStyle.success)
    async def callback(self, button, interaction):
        button.style = discord.ButtonStyle.danger if button.style == discord.ButtonStyle.success else discord.ButtonStyle.success

        self.ctx.bot.minecord.update_one({"_id":self.ctx.author.id}, {"$set": {"treasure": not (self.db["virtualfisher"]["treasure"])}})
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label='Fishing', style=discord.ButtonStyle.success)
    async def callback2(self, button, interaction):
        button.style = discord.ButtonStyle.danger if button.style == discord.ButtonStyle.success else discord.ButtonStyle.success

        self.ctx.bot.minecord.update_one({"_id":self.ctx.author.id}, {"$set": {"fish": not (self.db["virtualfisher"]["fish"])}})
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label='Worker', style=discord.ButtonStyle.success)
    async def callback3(self, button, interaction):
        button.style = discord.ButtonStyle.danger if button.style == discord.ButtonStyle.success else discord.ButtonStyle.success

        self.ctx.bot.minecord.update_one({"_id":self.ctx.author.id}, {"$set": {"worker": not (self.db["virtualfisher"]["worker"])}})
        await interaction.response.edit_message(view=self)

    @discord.ui.select(placeholder='Currently editing: Virtual Fisher', min_values=1, max_values=1, options=[
        discord.SelectOption(label='Minecord', description='Edit Minecord Settings'),
        discord.SelectOption(label='Minecord Classic', description='Edit Minecord Classic Settings')
    ])
    async def select_callback(self, select, interaction):
        self.value = select.values[0]
        self.stop()

class Event(Modal):
    def __init__(self) -> None:
        super().__init__(title = "Event")
        self.title = "Event"
        self.add_item(InputText(label="How long do you want the event to last?", placeholder="1d 2h 3m 4s"))
    
    async def callback(self, interaction: discord.Interaction):
        self.value = self.children[0].value
        await interaction.response.defer()
        self.interaction = interaction
        self.stop()