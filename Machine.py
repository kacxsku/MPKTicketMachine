from CoinExtractor import CoinExtractor
from Tickets import *


class Machine(CoinExtractor, Tickets):

    total_cost = 0

    def __init__(self):
        super().__init__()

    def calculateAllChosenTicketsPrice(self, choosen, value):
        self.total_cost += Tickets.ticket[str(choosen)]*int(value)

    def getMoneySum(self):
        return self.total_cost

    def substraction(self, v):
        return self.total_cost-v
