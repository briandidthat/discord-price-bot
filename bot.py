import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from spot import SpotFetcher, SpotPrice

# load environment variables
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="$", intents=intents)

logger = logging.getLogger(name="bot.logger")
logger.setLevel(logging.DEBUG)


@bot.event
async def on_ready():
    print("price bot is online")


@bot.command(name="spot", description="get the current spot price of a token")
async def spot(ctx, symbol: str = None):
    if symbol is None:
        await ctx.send("You must provide a symbol. Try again")
        return

    caller = ctx.author.name
    response: SpotPrice = SpotFetcher.get_spot_price(symbol, caller)

    await ctx.send(f"{response.base}: {response.amount}")


@bot.command(name="historical-spot", description="get the historical spot price of a token")
async def historical_spot(ctx, symbol: str = None, date: str = None):
    if symbol is None or date is None:
        await ctx.send("Symbol and date cannot be null. Try again")
        return

    caller = ctx.author.name
    response: SpotPrice = SpotFetcher.get_historical_spot_price(symbol, date, caller)
    response_text: str = f"{response.base}: {response.amount}. {response.date}"

    await ctx.send(response_text)


@bot.command(name="batch-spot", description="get the current spot price for multiple tokens")
async def batch_spot(ctx, *args):
    if len(args) == 0 or len(args) > 5:
        await ctx.send("Length of symbols list must be 1-5. Try again")
        return

    caller = ctx.author.name
    response: list[SpotPrice] = SpotFetcher.get_batch_spot_price(args, caller)
    response_text: str = ""

    for spot_price in response:
        response_text += f"{spot_price.base}: {spot_price.amount}\n"

    await ctx.send(response_text)


@bot.command(name="batch-historical-spot", description="get the historical spot price for multiple tokens")
async def batch_historical_spot(ctx, *args):
    if len(args) == 0 or len(args) > 5:
        await ctx.send("Length of symbols list must be 1-5. Try again")
        return

    caller = ctx.author.name

    # split the strings at the colon to separate symbol and date and save in list
    request_tuples = [s.split(":") for s in args]
    requests = dict()

    print(requests)

    for symbol, date in request_tuples:
        requests[symbol] = date

    response: list[SpotPrice] = SpotFetcher.get_batch_historical_spot_price(requests, caller)
    response_text: str = ""

    for spot_price in response:
        response_text += f"{spot_price.base}: {spot_price.amount}. Date: {spot_price.date}\n"

    await ctx.send(response_text)


bot.run(token=TOKEN)
