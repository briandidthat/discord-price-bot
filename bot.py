import os

import discord
from dotenv import load_dotenv

# load environment variables
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"price bot is online {client.user}")


@client.event
async def on_message(message):
    # if the author of the message is the bot itself, ignore
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        await message.channel.send("whatsup mate")


client.run(token=TOKEN)
