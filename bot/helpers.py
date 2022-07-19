import discord
from typing import Dict, Union


async def open_account(
    user: Union[discord.Member, discord.User], bot: discord.Bot
) -> None:

    if (await bot.virtualfisher.count_documents({"_id": user.id})) != 0:
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
        await bot.minecordclassic.insert_one(post1)

        post2 = {
            "_id": user.id,
            "treasure": True,
            "fish": True,
            "worker": True,
            "cooldown": 3.0,
            "response": "% & cooldown elapsed! \nCurrent cooldown is `$ seconds`!",
        }
        await bot.virtualfisher.insert_one(post2)
    return True


async def fetch_user(user: Union[discord.Member, discord.User], bot: discord.Bot) -> dict:
    """Fetches user data from database

    Args:
        user (Union[discord.Member, discord.User]): The user to fetch data for
        bot (discord.Bot): The bot instance

    Returns:
        dict: The user data
    """
    settings = {}
    settings["minecordclassic"] = await bot.db["minecord-classic"].find_one({"_id": user.id})
    settings["virtualfisher"] = await bot.db["virtual-fisher"].find_one({"_id": user.id})
    return settings


async def fetch_event(guild: discord.Guild, bot: discord.Bot) -> dict:

    return await bot.minecord.find_one({"_id": guild.id})


async def convert_to_seconds(s: str) -> int:
    seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
    try:
        return int(s[:-1]) * seconds_per_unit[s[-1]]
    except:
        return "Invalid time unit!"
