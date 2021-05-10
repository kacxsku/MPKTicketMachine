from CoinExtractor import CoinExtractor
from Tickets import *


class Machine(CoinExtractor):
    _sum = 0

    def __init__(self):
        super().__init__()
        pass

    def buyTicket(self, ticketPrice):
        self._sum += ticketPrice #cena biletu

    def end(self):
        self._sum = 0
        pass

