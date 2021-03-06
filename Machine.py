from CoinExtractor import CoinExtractor
from Tickets import *
from decimal import *
from exceptions import *

getcontext().prec = 3  #setting precision to 2 numbers after the comma


class Machine(CoinExtractor, Tickets):
    """class representing ticket machine"""

    def __init__(self):
        super().__init__()
        self.coinExtractor = CoinExtractor()
        self._actuallyInMachine = [Decimal(str(1.0)), Decimal(str(2.0))]
        self._recently_added_coins = []
        self._total_cost = Decimal(str(0))

    def returnChange(self, change):
        '''algorithm for spending the change, returns string displayed on message box after transaction'''
        changeList = []
        for i in [float(c) for c in sorted(self._actuallyInMachine, reverse=True) if c <= float(change)]:
            if i <= change:
                changeList.append(Decimal(str(i)))
                change -= Decimal(str(i))
            if change == 0:
                self._actuallyInMachine = [Decimal(str(k)) for k in self._actuallyInMachine if k not in changeList]
                return "Twoja reszta :\n" + str(", ".join([str(float(i)) for i in changeList]))
            if change <0:
                break
        else:
            if change == Decimal(str(0)) and len(changeList) == Decimal(str(0)):
                return "Kupiłeś bilet za odliczoną kwotę"
            elif change > 0:
                for i in self._recently_added_coins:
                    if i in self._actuallyInMachine:
                        self._actuallyInMachine.remove(i)
                return "Nie mogę wydać ci reszty\n Nie kupiłeś biletu\n oddaje: " + str(
                    ", ".join([str(float(i)) for i in self._recently_added_coins]))

    @staticmethod
    def checkValue(spinboxValue):
        '''Check if value from spinbox is inteeger value or if it's negative number'''
        try:
            int(spinboxValue)
        except ValueError:
            raise NotIntValueError("Liczba pieniędzy musi być całkowita")
        if int(spinboxValue) <= 0:
            raise NegativeNumberValueError("Liczba pieniędzy musi być dodatnia")

    def setTotalCost(self, value):
        '''set total cost of tickets'''
        self._total_cost = Decimal(str(value))

    def getTotalCost(self):
        '''get total cost of tickets'''
        return self._total_cost

    def addMoneyToMachine(self, money):
        '''add thrown into machine moneys to list'''
        self._actuallyInMachine.append(Decimal(str(money)))
        self._recently_added_coins.append(Decimal(str(money)))

    def getAcctuallyInMachineSum(self):
        '''get sum of money in macjine'''
        return sum(self._actuallyInMachine)

    def setRecenlty(self):
        self._recently_added_coins = []

    def clearList(self):
        '''helper for tests'''
        self._actuallyInMachine =[]
