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