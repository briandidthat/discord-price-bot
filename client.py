import discord

from spot import SpotFetcher


class Client(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)

    async def on_ready(self):
        print(f"price bot is online {self.user}")

    async def on_message(self, message: discord.Message):
        # if the author of the message is the bot itself, ignore
        if message.author == self.user:
            return

        response = SpotFetcher.get_spot_price("BTC")

        if self.user.mentioned_in(message):
            await message.channel.send(response.amount)
