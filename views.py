import discord

class Invite(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Invite me!',
            style=discord.ButtonStyle.link,
            url=
            "https://discord.com/oauth2/authorize?bot_id=836581672811495465&permissions=321536&scope=bot%20applications.commands",
            row=1)


class Invite2(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Alternative link.',
            style=discord.ButtonStyle.link,
            url=
            "https://discord.com/oauth2/authorize?bot_id=931981494887534602&permissions=321536&scope=bot%20applications.commands",
            row=1)

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