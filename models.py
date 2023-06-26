class SpotPrice:
    def __init__(self, response: dict) -> None:
        self.base = response["base"]
        self.currency = response["currency"]
        self.amount = response["amount"]
        self.date = response["date"]


class Request:
    def __init__(self, symbol: str, date: str) -> None:
        self.symbol = symbol
        self.date = date

    def serialize(self):
        return {"symbol": self.symbol, "date": self.date}


class BatchRequest:
    def __init__(self, requests: []) -> None:
        self.requests: list[Request] = requests

    def add_request(self, request: Request):
        self.requests.append(request)

    def serialize(self):
        return {"requests": [r.serialize() for r in self.requests]}


class Statistic:
    def __init__(self, response: dict[str, str]) -> None:
        self.symbol = response["symbol"]
        self.price_change = response["priceChange"]
        self.percent_change = response["percentChange"]
        self.time_delta = response["timeDelta"]
