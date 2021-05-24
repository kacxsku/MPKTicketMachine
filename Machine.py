from CoinExtractor import CoinExtractor
from Tickets import *
from decimal import *
from exceptions import *

getcontext().prec = 3


class Machine(CoinExtractor, Tickets):
    """class representing ticket machine"""
    _total_cost = Decimal('0')
    _actuallyInMachine = []

    def __init__(self):
        super().__init__()
        self.coinExtractor = CoinExtractor()

    def calculateAllChosenTicketsPrice(self, choosen, value):
        '''calculate choosen ticket price'''
        self._total_cost += Decimal(str(Tickets.ticket[str(choosen)]*int(value)))

    def getMoneySum(self):
        '''return money sum of total cost'''
        return Decimal(str(self._total_cost))

    def addMoneyToMachine(self, money):
        '''add thrown into machine moneys to list'''
        self._actuallyInMachine.append(money)

    # nie zwraca monety jak nie ma czym wydac error
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
                self._actuallyInMachine.remove(i)
            else:
                if change == 0 and len(changeList)==0:
                    return "Kupiłeś bilet za odliczoną kwotę"
                elif change != 0: #error
                    if len(changeList) == 0:
                        changeList.append(change)
                    return "Nie mogę wydać ci reszty\n Nie kupiłeś biletu\n oddaje:"+str(", ".join([str(float(i)) for i in changeList]))
        return "Twoja reszta :\n" + str(", ".join([str(float(i)) for i in changeList]))

    def substraction(self, change):
        '''substraction returns total cost of choosen tickets'''
        self._total_cost = Decimal(str(self._total_cost)) - Decimal(str(change))
        return Decimal(str(self._total_cost))

    def checkValue(self, spinboxValue):
            '''Check if value from spinbox is inteeger value or if it's negative number'''
            try:
                int(spinboxValue)
            except ValueError:
                raise NotIntValueError()
            if int(spinboxValue) <= 0:
                raise NegativeNumberValueError()

