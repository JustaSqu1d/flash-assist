async def open_account(user, bot):
    
    if bot.minecord.count_documents({"_id": user.id}) != 0:
        return
    else:
        post1 = {"_id": user.id, "efficiency": False, "armor": 0, "dragoncd": 5, "mine": True, "fight": True, "chop": True, "ed": True, "response": "% & command cooldown elapsed! \nCurrent cooldown is `$ seconds`!"}
        bot.minecordclassic.insert_one(post1)

        post2 = {"_id": user.id, "efficiency": False, "mine": True, "fight": True, "chop": True, "ed": True, "response": "% & command cooldown elapsed! \nCurrent cooldown is `$ seconds`!"}
        bot.minecord.insert_one(post2)

        post3 = {"_id": user.id, "treasure": True, "fish": True, "worker": True, "response": "% & boost elapsed! \nCurrent cooldown is `$ seconds`!"}
        bot.virtualfisher.insert_one(post3)
    return True

def fetch_user(user, bot):

    settings = {}
    settings["minecord"] = bot.minecord.find_one({"_id": user.id})
    settings["minecordclassic"] = bot.minecordclassic.find_one({"_id": user.id})
    settings["virtualfisher"] = bot.minecordclassic.find_one({"_id": user.id})
    return settings

