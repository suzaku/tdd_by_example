import abc


class Expression(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def reduce(self, bank, to):
        pass

    def plus(self, addend):
        return Sum(self, addend)


class Money(Expression):

    def __init__(self, amount, currency):
        self._amount = amount
        self.currency = currency

    @staticmethod
    def dollar(amount):
        return Money(amount, "USD")

    @staticmethod
    def franc(amount):
        return Money(amount, "CHF")

    def times(self, multiplier):
        return Money(self._amount * multiplier, self.currency)

    def reduce(self, bank, to):
        rate = bank.rate(self.currency, to)
        return Money(self._amount / rate, to)

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.currency == other.currency and
                self._amount == other._amount)

    def __repr__(self):
        return '%s %s' % (self._amount, self.currency)

    __str__ = __repr__


class Bank(object):

    def __init__(self):
        self.rates = {}

    def add_rate(self, from_, to_, rate):
        self.rates[(from_, to_)] = rate

    def reduce(self, source, to):
        return source.reduce(self, to)

    def rate(self, from_, to):
        if from_ == to:
            return 1
        return self.rates.get((from_, to))


class Sum(Expression):

    def __init__(self, augend, addend):
        self.augend = augend
        self.addend = addend

    def reduce(self, bank, to):
        return Money(bank.reduce(self.augend, to)._amount +
                     bank.reduce(self.addend, to)._amount, to)

    def times(self, multiplier):
        return Sum(self.augend.times(multiplier),
                   self.addend.times(multiplier))
