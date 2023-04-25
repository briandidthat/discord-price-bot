import discord

from spot import SpotFetcher, SpotPrice


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

        if self.user.mentioned_in(message):
            spot_prices: list[SpotPrice] = SpotFetcher.get_multiple_spot_prices(["BTC", "ETH", "CRV"])
            response = [f"{s.base}: {s.amount} \n" for s in spot_prices]
            response_message = "".join(response)

            await message.channel.send(response_message)
