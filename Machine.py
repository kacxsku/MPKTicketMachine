from CoinExtractor import CoinExtractor
from Tickets import *
from decimal import *


class Machine(CoinExtractor, Tickets):

    _total_cost = Decimal(0)
    _actuallyInMachine = []

    def __init__(self):
        super().__init__()

    def calculateAllChosenTicketsPrice(self, choosen, value):
        self._total_cost += Decimal(Tickets.ticket[str(choosen)]*int(value))

    def getMoneySum(self):
        return Decimal(self._total_cost)

    def addMoneyToMachine(self, money):
        self._actuallyInMachine.append(Decimal(money))

    def returnChange(self, change):
        changeList = []
        if change in self._actuallyInMachine:
            changeList.append(change)
        else:
            for i in [c for c in self._actuallyInMachine if c <= change]:
                changeList.append(i)
                self._actuallyInMachine.pop(i)
            else:
                return []
        return changeList

    def substraction(self, change):
        self._total_cost = Decimal(self._total_cost) - Decimal(change)
        return Decimal(self._total_cost)
