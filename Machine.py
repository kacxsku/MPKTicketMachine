from decimal import Decimal

from CoinExtractor import CoinExtractor
from Tickets import *


class Machine(CoinExtractor,Tickets):
    _sum = 0

    def __init__(self):
        super().__init__()
        self.total_cost = 0


    def calcualteAllChoosenTicketsPrice(self,choosen,value):
        print('dupa')
        self.total_cost += Tickets.ticket[str(choosen)]*int(value)
        print(self.total_cost)

    def getMoneySum(self):
        return self._sum