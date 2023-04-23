import os

from dotenv import load_dotenv

from client import Client

# load environment variables
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

client = Client()

client.run(token=TOKEN)
