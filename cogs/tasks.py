import discord
from discord.ext import commands, tasks
import time as t
import os
from helpers import api_key, page_id, metric_id
from datetime import time, timezone
from replit import db

class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily.start()
        self.post_latency.start()

    def cog_unload(self):
        self.daily.cancel()
        self.post_latency.cancel()

    @tasks.loop(
        time=time(hour=0, minute=0, second=0, tzinfo=timezone.utc)
    )
    async def daily(self):
        for user in db.keys():
            if db[user]["vfdaily"]:
                person = await self.bot.fetch_user(user)
                embed = discord.Embed(title = "Reminder: Claim your Dailies!", color = discord.Color.green())
                embed.set_footer(text="You can disable reminders with /config")
                person.send()

    @tasks.loop(minutes=1)
    async def post_latency(self):
        if not(self.bot.is_ready()):
            await self.bot.wait_until_ready()
        ts = t.time()
        value = int(self.bot.latency*1000)
        os.system(f""" curl https://api.statuspage.io/v1/pages/{page_id}/metrics/data -H \"Authorization: OAuth {api_key}\" -X POST -d \"data[{metric_id}][][timestamp]={ts}\" -d \"data[{metric_id}][][value]={value}\" """)
        os.system("clear")

def setup(bot):
    bot.add_cog(Tasks(bot))