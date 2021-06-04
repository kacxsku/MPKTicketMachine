from CoinExtractor import CoinExtractor
from Tickets import *
from decimal import *
from exceptions import *

getcontext().prec = 3


class Machine(CoinExtractor, Tickets):
    """class representing ticket machine"""


    def __init__(self):
        super().__init__()
        self.coinExtractor = CoinExtractor()
        self._actuallyInMachine = []
        self._recently_added_coins = []

    def returnChange(self, change):
        '''algorithm for spending the change, returns string displayed on message box after transaction'''
        changeList = []
        if change in self._actuallyInMachine:
            changeList.append(change)
        else:
            for i in [float(c) for c in self._actuallyInMachine if c <= float(change)]:
                if change == 0:
                    break
                changeList.append(Decimal(str(i)))
                change -= Decimal(str(i))
                # self._actuallyInMachine.remove(i)
            else:
                if change == 0 and len(changeList) == 0:
                    self._actuallyInMachine = [i for i in self._actuallyInMachine if i not in changeList]
                    return "Kupiłeś bilet za odliczoną kwotę"
                elif change != 0:
                    return "Nie mogę wydać ci reszty\n Nie kupiłeś biletu\n oddaje:"+str(", ".join([str(float(i)) for i in self._recently_added_coins]))
        return "Twoja reszta :\n" + str(", ".join([str(float(i)) for i in changeList]))

    def checkValue(self, spinboxValue):
            '''Check if value from spinbox is inteeger value or if it's negative number'''
            try:
                int(spinboxValue)
            except ValueError:
                raise NotIntValueError()
            if int(spinboxValue) <= 0:
                raise NegativeNumberValueError()

    def setTotalCost(self,value):
        self._total_cost = decimal(str(value))

    def getTotalCost(self):
        return self._total_cost

    def addMoneyToMachine(self, money):
        '''add thrown into machine moneys to list'''
        self._actuallyInMachine.append(Decimal(str(money)))
        self._recently_added_coins.append(str(money))

    def getAcctuallyInMachineSum(self):
        return sum(self._actuallyInMachine)


