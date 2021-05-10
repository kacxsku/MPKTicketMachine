from decimal import Decimal

from CoinExtractor import CoinExtractor
from Tickets import *


class Machine(CoinExtractor, Tickets):

    total_cost = 0

    def __init__(self):
        super().__init__()

###suma nie zmienia sie dziwne!!!!
    def calcualteAllChoosenTicketsPrice(self,choosen,value):
        self.total_cost += Tickets.ticket[str(choosen)]*int(value)
       # print(self.total_cost)

    def getMoneySum(self):
        print(self.total_cost)
        return self.total_cost

    def substraction(self,v):
        return self.total_cost-v


