from discord.ext import commands, tasks
import time as t
import os
from datetime import time

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
        ts = t.time()
        value = int(self.bot.latency*1000)
        self.bot.statuspage.metrics.submit_data(
            metric_id = metric_id,
            timestamp = ts,
            value = value
        )

    @tasks.loop(hours=1)
     async def post_logs(self):
         if not(self.bot.is_ready()):
             await self.bot.wait_until_ready()
36	-         await sleep(2)
37	-         channel = await self.bot.fetch_channel(966024569444008076)
38	-         with open('discord.log', 'rb') as fp:
39	-             print(fp)
40	-             await channel.send("Logs:",file=File(fp, '..discord.log'))

def setup(bot):
    bot.add_cog(Tasks(bot))