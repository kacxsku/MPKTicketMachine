

class Tickets:
    """class for representing tickets and its value"""
    ticket = {"20 min ulgowy": 2,
                             "20 min normalny": 4,
                             "40 min ulgowy": 3,
                             "40 min normalny": 5.50,
                             "60 min ulgowy": 4,
                             "60 min normalny": 8}

    def getTicketPrice(self, key):
        return self.ticket.get(key)
