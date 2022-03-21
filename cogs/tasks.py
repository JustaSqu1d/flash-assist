"""
@tasks.loop(seconds=1)
async def daily():
    time = datetime.datetime.now().time()
    time = str(time)
    print(time)
"""

import discord
from discord.ext import commands, tasks
from datetime import datetime
import time, os
from helpers import api_key, page_id, metric_id

class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily.start()
        self.post_latency.start()

    def cog_unload(self):
        self.daily.cancel()
        self.post_latency.cancel()

    @tasks.loop(seconds=1)
    async def daily(self):
        time = datetime.now().time()
        time = str(time)
        time = time.split(".")[0]
        if time == "00:00:00":
            #do stuff
            pass

    @tasks.loop(minutes=1)
    async def post_latency(self):
        if not(self.bot.is_ready()):
            await self.bot.wait_until_ready()
        ts = time.time()
        value = int(self.bot.latency*1000)
        os.system(f""" curl https://api.statuspage.io/v1/pages/{page_id}/metrics/data -H \"Authorization: OAuth {api_key}\" -X POST -d \"data[{metric_id}][][timestamp]={ts}\" -d \"data[{metric_id}][][value]={value}\" """)
        os.system("clear")

def setup(bot):
    bot.add_cog(Tasks(bot))