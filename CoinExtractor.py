from decimal import Decimal
from Tickets import *

class CoinExtractor(Tickets):
    """All available moneys"""
    _moneys = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0]


    def __init__(self):
        super().__init__()
        self._total_cost = Decimal('0')
    def calculateAllChosenTicketsPrice(self, choosen, value):
        '''calculate choosen ticket price'''
        self._total_cost += Decimal(str(Tickets.ticket[str(choosen)]*int(value)))

    def getMoneySum(self):
        '''return money sum of total cost'''
        return Decimal(str(self._total_cost))




    def getMoneyList(self):
        '''return available moneys list'''
        return self._moneys

    def substraction(self, change):
        '''substraction returns total cost of choosen tickets'''
        self._total_cost = Decimal(str(self._total_cost)) - Decimal(str(change))
        return Decimal(str(self._total_cost))
