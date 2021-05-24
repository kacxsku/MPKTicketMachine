from decimal import Decimal


class CoinExtractor:
    """All available moneys"""
    _moneys = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0]

    def __init__(self):
        self._available_moneys = []  # TODO: check it

    def add_coin(self, money):
        if not isinstance(money, Moneta):
            raise NotImplementedError()  # TODO: error
        self._available_moneys.append(money)

    def remove_coin(self, money):
        self._available_moneys.pop(money)

    def moneys_sum(self):  # TODO:
        return sum(m.getValue() for m in self._available_moneys)

    def getMoneyList(self):
        return self._moneys
