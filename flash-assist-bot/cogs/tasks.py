from discord.ext import commands, tasks
import time as t
import os
from datetime import time
from asyncio import sleep
from discord import File

metric_id = 'btv9x2yn5b90'

class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.post_latency.start()

    def cog_unload(self):
        self.post_latency.cancel()

    @tasks.loop(minutes=1)
    async def post_latency(self):
        
        if not(self.bot.is_ready()):
            await self.bot.wait_until_ready()
        #TODO 

    @tasks.loop(hours=1)
    async def post_logs(self):
        if not(self.bot.is_ready()):
            await self.bot.wait_until_ready()
        await sleep(2)
        channel = await self.bot.fetch_channel(966024569444008076)
        with open('discord.log', 'rb') as fp:
            print(fp)
            await channel.send("Logs:",file=File(fp, '..discord.log'))

def setup(bot):
    bot.add_cog(Tasks(bot))