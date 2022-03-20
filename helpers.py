from replit import db
import time, random, os, asyncio

api_key = os.environ['SPKEY']
page_id = 'm4j4kdx61gkt'
metric_id = 'btv9x2yn5b90'
api_base = 'api.statuspage.io/v1'

async def post_ping(latency):
    total_points = int(60 / 5 * 24)
    latency = int(latency*1000)
    
    for i in range(total_points):
        ts = int(time.time()) - (i * 5 * 60)
        
        delta = random.randint(0,random.randint(3,5))
        if ((random.randint(1,100) % 2) == 0):
            latency -= delta
            value = latency
            latency += delta
            
        else:
            latency += delta
            value = latency
            latency -= delta
            
        result = os.system(f""" curl https://api.statuspage.io/v1/pages/{page_id}/metrics/data -H \"Authorization: OAuth {api_key}\" -X POST -d \"data[{metric_id}][][timestamp]={ts}\" -d \"data[{metric_id}][][value]={value}\" """)
        os.system("clear")
        
        await asyncio.sleep(1)
        
        
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

        db[str(user.id)]["treasure"] = True
        db[str(user.id)]["fish"] = True
        db[str(user.id)]["worker"] = True
        
        db[str(
            user.id
        )]["response"] = "% & boost/command cooldown elapsed! \nCurrent cooldown is `$ seconds`!"

    return True