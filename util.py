import locale

# this sets locale to the current Operating System value
locale.setlocale(locale.LC_ALL, "en_US.UTF-8")


class SpotPrice:
    def __init__(self, response: dict) -> None:
        self.base = response["base"]
        self.currency = response["currency"]
        self.amount = locale.currency(float(response["amount"]), grouping=True, symbol=True)
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
        self.token = response["token"]
        self.price_change = response["price_change"]
        self.percent_change = response["percent_change"]
        self.time_delta = response["time_delta"]
