"""
Execution layer astratto + OANDA broker (paper/live).
"""

from dataclasses import dataclass

@dataclass
class Order:
    symbol: str
    side: str   # "BUY" | "SELL"
    qty: float
    price: float | None = None
    client_tag: str | None = None
    sl: float | None = None
    tp: float | None = None

class Broker:
    def place_order(self, order: Order): raise NotImplementedError
    def close_all(self, symbol: str): raise NotImplementedError
    def positions(self): raise NotImplementedError

class PaperBroker(Broker):
    def __init__(self, starting_cash: float = 10000.0):
        self.cash = starting_cash
        self.positions_book = []

    def place_order(self, order: Order):
        # skeleton: append to book (riempimento immediato)
        self.positions_book.append(order)
        return {"status":"filled","order":order}

    def close_all(self, symbol: str):
        self.positions_book = [p for p in self.positions_book if p.symbol != symbol]

    def positions(self):
        return list(self.positions_book)

class OandaBroker(Broker):
    def __init__(self, api_key: str, account_id: str, account_type: str = "practice"):
        import oandapyV20
        self.account_id = account_id
        self.client = oandapyV20.API(access_token=api_key)
        self.is_practice = (account_type == "practice")

    def place_order(self, order: Order):
        # TODO: mappare su OrdersCreate endpoint + client extensions (clientTag=order.client_tag)
        # return response dict
        return {"status":"TODO", "note":"Implementa endpoint OANDA OrdersCreate"}

    def close_all(self, symbol: str):
        # TODO: mappare su PositionsClose endpoint
        return {"status":"TODO"}

    def positions(self):
        # TODO: mappare su Positions endpoint
        return []
