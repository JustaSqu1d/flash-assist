import discord
from discord.ext import commands, tasks
import time as t
import os
from helpers import api_key, page_id, metric_id
from datetime import time, timezone
from replit import db
import aiohttp
import datetime
from discord import Webhook

class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.post_latency.start()
        self.update_status.start()

    def cog_unload(self):
        self.update_status.cancel()
        self.post_latency.cancel()

    @tasks.loop(minutes=1)
    async def post_latency(self):
        if not(self.bot.is_ready()):
            await self.bot.wait_until_ready()
        ts = t.time()
        value = int(self.bot.latency*1000)
        os.system(f""" curl https://api.statuspage.io/v1/pages/{page_id}/metrics/data -H \"Authorization: OAuth {api_key}\" -X POST -d \"data[{metric_id}][][timestamp]={ts}\" -d \"data[{metric_id}][][value]={value}\" """)
        os.system("clear")

    @tasks.loop(minutes=1)
    async def update_status(self):
        if not(self.bot.is_ready()):
            await self.bot.wait_until_ready()
        async with aiohttp.ClientSession() as session:
            async with session.get('https://m4j4kdx61gkt.statuspage.io/api/v2/status.json') as r:
                response = r.json
                if response["status"] != "All Systems Operational":
                     async with aiohttp.ClientSession() as session2:
                        webhook = Webhook.from_url(os.environ['WHURL'], session=session2)
                        async with session.get('https://m4j4kdx61gkt.statuspage.io/api/v2/incidents/unresolved.json') as r2:
                            response2 = r2.json
                        incident = response2["incidents"][0]
                        embed = discord.Embed(title=incident["name"], url=incident["shortlink"])
                        
                        for update in incident["incident_updates"]:
                            embed.add_field(name=update["status"], value = update["body"], inline = False)
                            timestamp1 = update["created_at"].split("-")
                            timestamp2 = timestamp1[2].split(":")
                            time = datetime.datetime(
                                year=int(timestamp1[0]),
                                month=int(timestamp1[1]),
                                day=int(timestamp1[2]),
                                hour=int(timestamp2[0].split("T")[1]),
                                minute=int(timestamp2[1]),
                                second=int(timestamp2[2].split(".")[0])
                            )
                            
                        
                        await webhook.send(embed=embed)

def setup(bot):
    bot.add_cog(Tasks(bot))