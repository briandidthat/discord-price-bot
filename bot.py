import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from spot import SpotFetcher, SpotPrice
from util import Request, BatchRequest, Statistic

# load environment variables
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="$", intents=intents)


@bot.event
async def on_ready():
    print("price bot is online")


@bot.command(name="spot", description="get the current spot price of a token")
async def spot(ctx, symbol: str = None):
    if symbol is None:
        await ctx.send("You must provide a symbol. Try again")
        return

    caller: str = ctx.author.name
    response: SpotPrice = SpotFetcher.get_spot_price(caller, symbol)

    await ctx.send(f"{response.base}: {response.amount}")


@bot.command(name="historical-spot", description="get the historical spot price of a token")
async def historical_spot(ctx, symbol: str = None, date: str = None):
    if symbol is None or date is None:
        await ctx.send("Symbol and date cannot be null. Try again")
        return

    caller: str = ctx.author.name
    response: SpotPrice = SpotFetcher.get_historical_spot_price(caller, symbol, date)
    response_text: str = f"{response.base}: {response.amount}. {response.date}"

    await ctx.send(response_text)


@bot.command(name="batch-spot", description="get the current spot price for multiple tokens")
async def batch_spot(ctx, *args):
    if len(args) == 0 or len(args) > 5:
        await ctx.send("Length of symbols list must be 1-5. Try again")
        return

    caller: str = ctx.author.name
    response: list[SpotPrice] = SpotFetcher.get_batch_spot_price(caller, args)
    response_text: str = ""

    for spot_price in response:
        response_text += f"{spot_price.base}: {spot_price.amount}\n"

    await ctx.send(response_text)


@bot.command(name="batch-historical-spot", description="get the historical spot price for multiple tokens")
async def batch_historical_spot(ctx, *args):
    if len(args) == 0 or len(args) > 5:
        await ctx.send("Length of symbols list must be 1-5. Try again")
        return

    caller: str = ctx.author.name
    # split the strings at the colon to separate symbol and date and save in list
    request_tuples = [tuple(s.split(":")) for s in args]
    # cute, but not readable
    # batch_request = BatchRequest([Request(symbol, date) for symbol, date in request_tuples])
    batch_request = BatchRequest([])

    for symbol, date in request_tuples:
        batch_request.add_request(Request(symbol, date))

    response: list[SpotPrice] = SpotFetcher.get_batch_historical_spot_price(caller, batch_request)
    response_text: str = ""

    for spot_price in response:
        response_text += f"{spot_price.base}: {spot_price.amount}. Date: {spot_price.date}\n"

    await ctx.send(response_text)


@bot.command(name="statistics", description="get the price statistics of a token for a period of time")
async def statistics(ctx, symbol: str = None, start_date: str = None, end_date: str = None):
    if symbol is None or start_date is None:
        await ctx.send("symbol and date cannot be null. Try again")

    caller: str = ctx.author.name

    response: Statistic = SpotFetcher.get_price_statistics(caller, symbol, start_date, end_date)
    response_text: str = f"**{response.symbol} stats from {start_date} to {end_date}**\n" \
                         f"Price change: {response.price_change}\n" \
                         f"Percent change: {response.percent_change}%\n" \
                         f"Timeline: {response.time_delta}"
    await ctx.send(response_text)


bot.run(token=TOKEN)
