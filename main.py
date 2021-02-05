"""

The main program.

-----------

Classes list:

No classes!

-----------

Functions list:

No functions!

"""

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from json import loads, dumps
from pathlib import Path
import logging
from create_logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

JSON_PATH = Path.cwd() / "goose_counter.json"

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="=")


def load_json(path: Path) -> dict:
    """
    Load JSON from a pathlib.Path JSON file.

    :param path: A pathlib.Path object that points to a JSON file.
    :return: The JSON as a dictionary.
    """
    return loads(s=path.read_text())


def save_json(json: dict, path: Path) -> None:
    """
    Save JSON to somewhere.

    :param json: A dictionary that is your JSON.
    :param path: A pathlib.Path that points to the JSON file.
    :return: None.
    """
    path.write_text(data=dumps(obj=json, sort_keys=True, indent=4))


@bot.event
async def on_ready() -> None:
    """
    Gets called when the bot has successfully connected to Discord.

    :return: None.
    """
    logger.info(f"{bot.user} has connected to {len(bot.guilds)} guild(s)!")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                        name=f"{json['count']} geese!"))


@bot.event
async def on_message(message: discord.message.Message) -> None:
    """
    Gets called on every message sent.

    :param message: The message discord.py will pass to us.
    :return: None.
    """
    if message.author == bot.user:
        return
    if json["config"]["message"] in message.content:
        json["count"] += 1
        save_json(json=json, path=JSON_PATH)
        logger.debug(f"Found goose {json['count']}!")
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                            name=f"{json['count']} geese!"))


json = load_json(path=JSON_PATH)

bot.run(token)
