class CoinExtractor:
    _moneys = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10, 20, 50]

    def __init__(self, money):
        if money not in self._moneys:
            raise NotImplementedError() #TODO: error
        self.money = money
        self._available_moneys = []  # TODO: check it

    def __init__(self):
        pass

    def add_coin(self, money):
        self._available_moneys.append(money)

    def remove_coin(self, money):
        self._available_moneys.pop(money)

    def moneys_sum(self): #TODO:
        return sum(self._available_moneys)

    def giveMoneyBack(self, price, amount):#TODO:::::
        change = sum(amount) - price
        back = []
        while change>0:
            #try:
            mValue = max(filter(lambda i: i<change,self._available_moneys))
            #except ValueError():

            #if mValue in self._available_moneys:
            back.append(mValue)
            change -= mValue
        else:
            self.giveMoneyBack(amount, 0)

    @classmethod
    def getMoneyList(self):
        return self._moneys


    #obsluga bledow
#Wylicz reszte