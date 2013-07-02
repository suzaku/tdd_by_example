from unittest import TestCase
from .money import Money, Bank, Sum

class MoneyTest(TestCase):

    def test_multiplication(self):
        five = Money.dollar(5)
        self.assertEqual(Money.dollar(10), five.times(2))
        self.assertEqual(Money.dollar(15), five.times(3))

    def test_equality(self):
        self.assertTrue(Money.dollar(5) == Money.dollar(5))
        self.assertFalse(Money.dollar(5) == Money.dollar(6))
        self.assertFalse(Money.franc(5) == Money.dollar(5))

    def test_currency(self):
        self.assertEqual("USD", Money.dollar(1).currency)
        self.assertEqual("CHF", Money.franc(1).currency)

    def test_simple_addtion(self):
        five = Money.dollar(5)
        bank = Bank()
        sum = five.plus(five)
        reduced = bank.reduce(sum, "USD")
        self.assertEqual(Money.dollar(10), reduced)

    def test_plus_return_sum(self):
        five = Money.dollar(5)
        result = five.plus(five)
        self.assertEqual(five, result.augend)
        self.assertEqual(five, result.addend)

    def test_reduce_sum(self):
        sum = Sum(Money.dollar(3), Money.dollar(4))
        bank = Bank()
        result = bank.reduce(sum, "USD")
        self.assertEqual(result, Money.dollar(7))

    def test_reduce_money(self):
        bank = Bank()
        result = bank.reduce(Money.dollar(1), "USD")
        self.assertEqual(Money.dollar(1), result)

    def test_reduce_money_different_currency(self):
        bank = Bank()
        bank.add_rate("CHF", "USD", 2)
        result = bank.reduce(Money.franc(2), "USD")
        self.assertEqual(Money.dollar(1), result)

    def test_identity_rate(self):
        self.assertEqual(1, Bank().rate("USD", "USD"))

    def test_mixed_addition(self):
        fiveBucks = Money.dollar(5)
        tenFrancs = Money.franc(10)
        bank = Bank()
        bank.add_rate("CHF", "USD", 2)
        result = bank.reduce(fiveBucks.plus(tenFrancs), "USD")
        self.assertEqual(Money.dollar(10), result)

    def test_sum_plus_money(self):
        fiveBucks = Money.dollar(5)
        tenFrancs = Money.franc(10)
        bank = Bank()
        bank.add_rate("CHF", "USD", 2)
        s = Sum(fiveBucks, tenFrancs).plus(fiveBucks)
        result = bank.reduce(s, "USD")
        self.assertEqual(Money.dollar(15), result)

    def test_sum_times(self):
        fiveBucks = Money.dollar(5)
        tenFrancs = Money.franc(10)
        bank = Bank()
        bank.add_rate("CHF", "USD", 2)
        s = Sum(fiveBucks, tenFrancs).times(2)
        result = bank.reduce(s, "USD")
        self.assertEqual(Money.dollar(20), result)
