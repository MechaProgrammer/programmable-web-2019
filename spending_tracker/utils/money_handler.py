from money.money import Money
from money.currency import Currency


def money(value: float) -> object:
    return Money(str(value), Currency.EUR)
