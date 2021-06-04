import unittest

from CoinExtractor import CoinExtractor
from Machine import Machine
from exceptions import *
from decimal import Decimal


class MyTestCase(unittest.TestCase):

    def test_should_return_no_change(self):
        machine = Machine()
        machine.calculateAllChosenTicketsPrice("20 min ulgowy", '1')
        machine.addMoneyToMachine('2')
        substracted_moneys = Decimal(machine.substraction('2'))
        self.assertEqual('Kupiłeś bilet za odliczoną kwotę',machine.returnChange(-substracted_moneys))

    def test_should_return_change(self):
        machine = Machine()
        machine.calculateAllChosenTicketsPrice("20 min ulgowy", '1')
        machine.addMoneyToMachine('1')
        substracted_moneys = Decimal(machine.substraction('1'))
        machine.addMoneyToMachine('0.5')
        substracted_moneys = Decimal(machine.substraction('0.5'))
        machine.addMoneyToMachine('1')
        substracted_moneys = Decimal(machine.substraction('1'))
        self.assertEqual("Twoja reszta :\n0.5",machine.returnChange(-substracted_moneys))

    def test_should_return_cant_return_change(self):
        machine = Machine()
        machine.calculateAllChosenTicketsPrice("20 min ulgowy", '1')
        machine.addMoneyToMachine('1')
        substracted_moneys = Decimal(machine.substraction('1'))
        machine.addMoneyToMachine('5')
        substracted_moneys = Decimal(machine.substraction('5'))
        self.assertEqual("Nie mogę wydać ci reszty\n Nie kupiłeś biletu\n oddaje:1.0, 5.0", machine.returnChange(-substracted_moneys))

    def test_adding(self):
        machine = Machine()
        for i in range(0,100):
            machine.addMoneyToMachine('0.01')
        self.assertEqual(1, machine.getAcctuallyInMachineSum())


    def test_should_return_sum_of_two_tickets_price(self):
        coinExtractor = CoinExtractor()
        coinExtractor.calculateAllChosenTicketsPrice("20 min ulgowy", '1')
        coinExtractor.calculateAllChosenTicketsPrice("20 min ulgowy", '1')
        self.assertEqual(Decimal(str(4)), coinExtractor.getMoneySum())

    def test_should_return_NotIntException(self):
        machine = Machine()
        with self.assertRaises(NotIntValueError):
            machine.checkValue("1.5")

    def test_should_return_NegativeNumberException(self):
        machine = Machine()
        with self.assertRaises(NegativeNumberValueError):
            machine.checkValue("-1")

    def test_should_correctly_return_price(self):
        machine = Machine()
        machine.calculateAllChosenTicketsPrice("20 min ulgowy", '1')
        machine.addMoneyToMachine('1')
        machine.calculateAllChosenTicketsPrice("20 min ulgowy", '1')
        substracted_moneys = Decimal(machine.substraction('1'))
        self.assertEqual(Decimal(str(3)), machine.getTotalCost())

if __name__ == '__main__':
    unittest.main()
