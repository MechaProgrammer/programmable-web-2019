# https://github.com/vimeo/py-money
from money.money import Money
from money.currency import Currency


def to_money(value: float) -> object:
    """Change float values to Money objects"""
    return Money(str(value), Currency.EUR)


def money_to_float(obj: object) -> float:
    """Change Money objects to float"""
    return float(obj.amount)


def add_objects(objs):
    """Add different Money objects"""
    total = Money('0', Currency.EUR)
    for arg in objs:
        total += arg
    return float(total.amount)


def money_add(*args):
    """Add float together by using Money objects
    Necessary only for currency operations
    """
    money_objs = list(map(to_money, [arg for arg in args]))
    return add_objects(money_objs)


