import datetime
import os

import requests
from dotenv import load_dotenv

from models import SpotPrice, Request, BatchRequest, Statistic

# load environment variables
load_dotenv()
price_server_url = os.getenv("PRICE_SERVER_URL")


class SpotFetcher:
    @staticmethod
    def get_health(caller: str) -> str:
        try:
            response = requests.get(f"{price_server_url}/healthz", headers={"caller": caller})
            return response.text
        except Exception as e:
            print(f"Http exception occurred. {e}")

    @staticmethod
    def get_spot_price(caller: str, symbol: str) -> SpotPrice:
        request = Request(symbol, "", "")
        try:
            response = requests.post(f"{price_server_url}/spot", json=request.serialize(),
                                     headers={"caller": caller, "Content-Type": "application/json"})
            return SpotPrice(response.json())
        except Exception as e:
            print(f"Http Exception occurred. {e}")

    @staticmethod
    def get_historical_spot_price(caller: str, symbol: str, date: str) -> SpotPrice:
        request = Request(symbol, date, "")
        try:
            response = requests.post(f"{price_server_url}/spot/historical", json=request.serialize(),
                                     headers={"caller": caller})
            return SpotPrice(response.json())
        except Exception as e:
            print(f"Http Exception occurred. {e}")

    @staticmethod
    def get_batch_spot_price(caller: str, symbols: list[str]) -> list[SpotPrice]:
        try:
            response = requests.get(f"{price_server_url}/spot/batch", json={"requests": symbols},
                                    headers={"caller": caller})
            data = response.json()
            responses = [SpotPrice(x) for x in data]
            return responses
        except Exception as e:
            print(f"Http Exception occurred. {e}")

    @staticmethod
    def get_batch_historical_spot_price(caller: str, batch_request: BatchRequest) -> list[SpotPrice]:
        try:
            response = requests.get(f"{price_server_url}/spot/historical/batch", json=batch_request.serialize(),
                                    headers={"caller": caller})
            data = response.json()
            responses = [SpotPrice(x) for x in data]
            return responses
        except Exception as e:
            print(f"Http Exception occurred. {e}")

    @staticmethod
    def get_price_statistics(caller: str, symbol: str, start_date: str, end_date: str = None):
        try:
            if end_date is None:
                end_date = datetime.date.today()

            response = requests.get(
                f"{price_server_url}/spot/statistics?symbol={symbol}&startDate={start_date}&end_date={end_date}",
                headers={"caller": caller})
            return Statistic(response.json())
        except Exception as e:
            print(f"Http Exception occurred. {e}")
