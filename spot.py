import locale
import os

import requests
from dotenv import load_dotenv

# load environment variables
load_dotenv()
price_server_url = os.getenv("PRICE_SERVER_URL")

# this sets locale to the current Operating System value
locale.setlocale(locale.LC_ALL, "en_US.UTF-8")


class SpotPrice:
    def __init__(self, response: dict) -> None:
        self.base = response["base"]
        self.currency = response["currency"]
        self.amount = locale.currency(float(response["amount"]), grouping=True, symbol=True)
        self.date = response["date"]


class SpotFetcher:
    @staticmethod
    def get_spot_price(symbol: str):
        try:
            response = requests.get(f"{price_server_url}?symbol={symbol}")
            return SpotPrice(response.json())
        except Exception as e:
            print(f"Http Exception occurred. {e.__str__()}")

    @staticmethod
    def get_historical_spot_price(symbol: str, date: str):
        try:
            response = requests.get(f"{price_server_url}?symbol={symbol}&date={date}")
            return SpotPrice(response.json())
        except Exception as e:
            print(f"Http Exception occurred. {e.__str__()}")

    @staticmethod
    def get_multiple_spot_prices(symbols: list[str]):
        try:
            response = requests.get(f"{price_server_url}/batch", json={"requests": symbols})
            data = response.json()
            responses = [SpotPrice(x) for x in data]
            return responses
        except Exception as e:
            print(f"Http Exception occurred. {e}")

    @staticmethod
    def get_multiple_historical_spot_prices(symbols: dict[str, str]):
        try:
            response = requests.get(f"{price_server_url}/historical", json={"requests": symbols})
            data = response.json()
            responses = [SpotPrice(x) for x in data]
            return responses
        except Exception as e:
            print(f"Http Exception occurred. {e}")
