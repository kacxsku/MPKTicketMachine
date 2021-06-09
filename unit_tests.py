import unittest

from CoinExtractor import CoinExtractor
from Machine import Machine
from exceptions import *
from decimal import Decimal


class MyTestCase(unittest.TestCase):
    '''class for unittest'''

    def test_should_return_no_change(self):
        '''gdy wrzucona jest wyliczona kwota to powinien zwrocic komunikat o zakupie biletow za odliczona kwote'''
        machine = Machine()
        machine.calculateAllChosenTicketsPrice("20 min ulgowy", '1')
        machine.addMoneyToMachine('2')
        substracted_moneys = Decimal(machine.substraction('2'))
        self.assertEqual('Kupiłeś bilet za odliczoną kwotę', machine.returnChange(-substracted_moneys))

    def test_should_return_change(self):
        '''gdy wrzucona jest nie wyliczona kwota to powinien zwrocic komunikat zwrocie reszty'''
        machine = Machine()
        machine.calculateAllChosenTicketsPrice("20 min ulgowy", '1')
        machine.addMoneyToMachine('1')
        machine.substraction('1')
        machine.addMoneyToMachine('0.5')
        machine.substraction('0.5')
        machine.addMoneyToMachine('1')
        substracted_moneys = Decimal(machine.substraction('1'))
        self.assertEqual("Twoja reszta :\n0.5", machine.returnChange(-substracted_moneys))

    def test_should_return_cant_return_change(self):
        '''gdy wrzucona jest nie wyliczona kwota i automat nie ma jak wydac reszty
         to powinien zwrocic komunikat o bledzie i zwrocic wrzucone monety'''
        machine = Machine()
        machine.calculateAllChosenTicketsPrice("20 min ulgowy", '1')
        machine.addMoneyToMachine('1')
        Decimal(machine.substraction('1'))
        machine.addMoneyToMachine('5')
        substracted_moneys = Decimal(machine.substraction('5'))
        self.assertEqual("Nie mogę wydać ci reszty\n Nie kupiłeś biletu\n oddaje: 1.0, 5.0",
                         machine.returnChange(-substracted_moneys))

    def test_adding(self):
        '''sprawdzenie dodawania 100 monet o wartosci 0.01'''
        machine = Machine()
        for _ in range(0, 100):
            machine.addMoneyToMachine('0.01')
        self.assertEqual(1, machine.getAcctuallyInMachineSum())

    def test_should_return_sum_of_two_tickets_price(self):
        '''sprawdzenie czy dodajac 2 bilety, kwota do zaplaty bedzie ich suma'''
        coinExtractor = CoinExtractor()
        coinExtractor.calculateAllChosenTicketsPrice("20 min ulgowy", '1')
        coinExtractor.calculateAllChosenTicketsPrice("20 min ulgowy", '1')
        self.assertEqual(Decimal(str(4)), coinExtractor.getMoneySum())

    def test_should_return_NotIntException(self):
        '''sprawdzenie czy jesli ilosc monet nie jest calkowita to czy zostanie rzucony wyjatek ->
         wyswietlony komunikat o bledzie'''
        machine = Machine()
        with self.assertRaises(NotIntValueError):
            machine.checkValue("1.5")

    def test_should_return_NegativeNumberException(self):
        '''sprawdzenie czy jesli ilosc monet nie jest dodatnia to czy zostanie rzucony wyjatek ->
         wyswietlony komunikat o bledzie'''
        machine = Machine()
        with self.assertRaises(NegativeNumberValueError):
            machine.checkValue("-1")

    def test_should_correctly_return_price(self):
        '''sprawdzenie czy dodajac bilet, nastepnie wrzucajac monete,
         a nastepnie dodajac kolejny bilet cena jest odpowiednia'''
        machine = Machine()
        machine.calculateAllChosenTicketsPrice("20 min ulgowy", '1')
        machine.addMoneyToMachine('1')
        machine.calculateAllChosenTicketsPrice("20 min ulgowy", '1')
        machine.substraction('1')
        self.assertEqual(Decimal(str(3)), machine.getTotalCost())


if __name__ == '__main__':
    unittest.main()
