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
    def get_spot_price(symbol: str, caller: str):
        try:
            response = requests.get(f"{price_server_url}?symbol={symbol}", headers={"caller": caller})
            return SpotPrice(response.json())
        except Exception as e:
            print(f"Http Exception occurred. {e}")

    @staticmethod
    def get_historical_spot_price(symbol: str, date: str, caller: str):
        try:
            response = requests.get(f"{price_server_url}?symbol={symbol}&date={date}", headers={"caller": caller})
            return SpotPrice(response.json())
        except Exception as e:
            print(f"Http Exception occurred. {e}")

    @staticmethod
    def get_batch_spot_price(symbols: list[str], caller: str):
        try:
            response = requests.get(f"{price_server_url}/batch", json={"requests": symbols}, headers={"caller": caller})
            data = response.json()
            responses = [SpotPrice(x) for x in data]
            return responses
        except Exception as e:
            print(f"Http Exception occurred. {e}")

    @staticmethod
    def get_batch_historical_spot_price(symbols: dict[str, str], caller: str):
        try:
            response = requests.get(f"{price_server_url}/historical", json={"requests": symbols},
                                    headers={"caller": caller})
            data = response.json()
            responses = [SpotPrice(x) for x in data]
            return responses
        except Exception as e:
            print(f"Http Exception occurred. {e}")
