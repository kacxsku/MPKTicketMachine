from CoinExtractor import CoinExtractor
from Tickets import *
from decimal import *

getcontext().prec = 3

class Machine(CoinExtractor, Tickets):

    _total_cost = Decimal('0')
    _actuallyInMachine = []

    def __init__(self):
        super().__init__()

    def calculateAllChosenTicketsPrice(self, choosen, value):
        self._total_cost += Decimal(str(Tickets.ticket[str(choosen)]*int(value)))

    def getMoneySum(self):
        return Decimal(str(self._total_cost))

    def addMoneyToMachine(self, money):
        self._actuallyInMachine.append(money)

    def returnChange(self, change):
        changeList = []
        if change in self._actuallyInMachine:
            changeList.append(change)
        else:
            for i in [float(c) for c in self._actuallyInMachine if c <= change]:
                if change==0:
                    break
                changeList.append(Decimal(str(i)))
                change -= Decimal(str(i))
                self._actuallyInMachine.remove(i)
            else:
                return []
        return changeList

    def substraction(self, change):
        self._total_cost = Decimal(str(self._total_cost)) - Decimal(str(change))
        return Decimal(str(self._total_cost))
