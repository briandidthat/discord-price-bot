import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

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
    await ctx.send(f"you requested {symbol}'s spot price")


@bot.command(name="historical-spot", description="get the historical spot price of a token")
async def historical_spot(ctx, symbol: str = None, date: str = None):
    if symbol is None or date is None:
        await ctx.send("Symbol and date cannot be null. Try again")
        return
    await ctx.send(f" requested {symbol}'s spot price on {date}")


@bot.command(name="multiple-spot", description="get the current spot price for multiple tokens")
async def multiple_spot(ctx, *args):
    if len(args) == 0 or len(args) > 5:
        await ctx.send("Length of symbols list must be 1-5. Try again")
        return

    await ctx.send(f"You requested ${args} spot price")


@bot.command(name="multiple-historical-spot", description="get the historical spot price for multiple tokens")
async def multiple_historical_spot(ctx, *args):
    if len(args) == 0 or len(args) > 5:
        await ctx.send("Length of symbols list must be 1-5. Try again")
        return

    # split the strings at the colon to separate symbol and date
    request_tuples = [s.split(":") for s in args]
    requests = dict()

    for symbol, date in request_tuples:
        requests[symbol] = date

    await ctx.send(f"You requested {requests} historical spot price")


bot.run(token=TOKEN)
