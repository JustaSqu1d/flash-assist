import discord
from typing import Dict, Union


async def open_account(
    user: Union[discord.Member, discord.User], bot: discord.Bot
) -> None:

    if bot.minecord.count_documents({"_id": user.id}) != 0:
        return
    else:
        post1 = {
            "_id": user.id,
            "efficiency": False,
            "armor": 0,
            "dragoncd": 5,
            "mine": True,
            "fight": True,
            "chop": True,
            "ed": True,
            "response": "% & command cooldown elapsed! \nCurrent cooldown is `$ seconds`!",
        }
        bot.minecordclassic.insert_one(post1)

        post2 = {
            "_id": user.id,
            "efficiency": False,
            "mine": True,
            "fight": True,
            "chop": True,
            "ed": True,
            "response": "% & command cooldown elapsed! \nCurrent cooldown is `$ seconds`!",
        }
        bot.minecord.insert_one(post2)

        post3 = {
            "_id": user.id,
            "treasure": True,
            "fish": True,
            "worker": True,
            "response": "% & boost elapsed! \nCurrent cooldown is `$ seconds`!",
        }
        bot.virtualfisher.insert_one(post3)
    return True


def fetch_user(user: Union[discord.Member, discord.User], bot: discord.Bot) -> dict:

    settings = {}
    settings["minecord"] = bot.minecord.find_one({"_id": user.id})
    settings["minecordclassic"] = bot.minecordclassic.find_one({"_id": user.id})
    settings["virtualfisher"] = bot.virtualfisher.find_one({"_id": user.id})
    return settings


def fetch_event(guild: discord.Guild, bot: discord.Bot) -> dict:

    return bot.minecord.find_one({"_id": guild.id})


async def convert_to_seconds(s: str) -> int:
    seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
    try:
        return int(s[:-1]) * seconds_per_unit[s[-1]]
    except:
        return "Invalid time unit!"
