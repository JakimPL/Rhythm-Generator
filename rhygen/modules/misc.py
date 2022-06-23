import math
from typing import List, Callable


def func(integers: List[int], f: Callable) -> int:
    value = integers[0]
    for integer in integers:
        value = f(value, integer)

    return value


def gcd(integers: List[int]) -> int:
    return func(integers, math.gcd)


def lcm(integers: List[int]):
    return func(integers, lambda x, y: x * y // math.gcd(x, y))


def is_power_of_two(value: int) -> bool:
    if value <= 0:
        return False

    while value != 1:
        if value % 2:
            return False
        value //= 2

    return True


def check_type(obj, obj_type):
    if not isinstance(obj, obj_type):
        raise TypeError('expected {}, got {}'.format(obj_type.__name__, type(obj_type)))
