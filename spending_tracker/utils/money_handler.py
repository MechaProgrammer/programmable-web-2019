from money.money import Money
from money.currency import Currency


# """https://github.com/vimeo/py-money"""
# """Module to handle calculations between money calculations"""


def to_money(value: float) -> object:
    """Change float values to Money objects"""
    return Money(str(value), Currency.EUR)


def money_to_float(obj: object) -> float:
    """Change Money objects to float"""
    return float(obj.amount)


def add_objects(objs) -> float:
    """Add different Money objects"""
    total = Money('0', Currency.EUR)
    for arg in objs:
        total += arg
    return float(total.amount)


def sub_objects(objs) -> float:
    """Subtract function"""
    total = Money('0', Currency.EUR)
    for arg in objs:
        total -= arg
    return float(total.amount)


def money_add(*args) -> float:
    """Add float together by using Money objects
    Necessary only for currency operations
    """
    money_objs = list(map(to_money, [0 if arg is None else arg for arg in args]))
    return add_objects(money_objs)


def money_subtract(*args) -> float:
    """Do subtract between give Money object argument"""
    money_objs = list(map(to_money, [0 if arg is None else arg for arg in args]))
    return sub_objects(money_objs)


print(money_subtract(-23, 4))
