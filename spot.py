import os

import requests
from dotenv import load_dotenv

# load environment variables
load_dotenv()
price_server_url = os.getenv("PRICE_SERVER_URL")


class Spot:
    @staticmethod
    def get_spot_price(symbol: str):
        response = requests.get(price_server_url + f"?symbol={symbol}")
        data = response.json()

        if response.status_code == 200:
            return data

        print(f"Http Exception occurred. {data}")
        return f"exception: {data}"

    @staticmethod
    def get_historical_spot_price(symbol: str, date: str):
        response = requests.get(price_server_url + f"?symbol={symbol}&date={date}")
        data = response.json()

        if response.status_code == 200:
            return data

        print(f"Http Exception occurred. {data}")
        return f"exception: {data}"

    @staticmethod
    def get_multiple_spot_prices(symbols: list[str]):
        response = requests.get(price_server_url, data={"requests": symbols})
        data = response.json()

        if response.status_code == 200:
            return data

        print(f"Http Exception occurred. {data}")
        return f"exception: {data}"

    @staticmethod
    def get_multiple_historical_spot_prices(symbols: dict[str, str]):
        response = requests.get(price_server_url + "/historical", data={"requests": symbols})
        data = response.json()

        if response.status_code == 200:
            return data

        print(f"Http Exception occurred. {data}")
        return f"exception: {data}"
