from replit import db
import aiohttp
import os

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