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
            selection = discord.ui.Select(min_values=1, max_values=5, placeholder="chose an operation")
            selection.add_option(label="current spot price", value="spot")
            selection.add_option(label="historical spot price", value="historical")
            selection.add_option(label="current price for multiple coins", value="multiple_spot")
            selection.add_option(label="historical price for multiple coins", value="multiple_historical")
            selection.add_option(label="statistics for a coin", value="statistics")

            view = discord.ui.View()
            view.add_item(selection)

            # spot_prices: list[SpotPrice] = SpotFetcher.get_multiple_spot_prices(["BTC", "ETH", "CRV"])
            # response = [f"{s.base}: {s.amount} \n" for s in spot_prices]
            # response_message = "".join(response)

            await message.channel.send("Hi.", view=view)
