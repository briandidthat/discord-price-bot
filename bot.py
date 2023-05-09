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
async def spot(ctx, symbol: str = commands.parameter(default="default")):
    print(symbol)
    if symbol == "default":
        await ctx.send("You must provide a symbol. Try again.")
        return
    await ctx.send(f"you asked for {symbol}")


bot.run(token=TOKEN)
