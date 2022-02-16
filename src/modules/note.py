from dataclasses import dataclass
from fractions import Fraction
from typing import Tuple, Union

from exceptions import NoteNotSupportedError
from misc import is_power_of_two


@dataclass
class Note:
    duration: Fraction
    pause: bool = False

    def __init__(self, argument):
        if isinstance(argument, Note):
            self.duration = argument.duration
            self.pause = argument.pause
        elif isinstance(argument, int):
            if argument == 0:
                raise ValueError('a value has to be non-zero')
            self.duration = Fraction(1, abs(argument))
            self.pause = argument < 0
        elif isinstance(argument, Fraction):
            self.duration = abs(argument)
            self.pause = argument < 0
        elif isinstance(argument, tuple):
            if len(argument) == 2 and all([isinstance(element, int) for element in argument]):
                self.duration = abs(Fraction(*argument))
                self.pause = (argument[0] * argument[1] < 0)
            else:
                raise ValueError('invalid tuple: {argument}, expected tuple[int, int]'.format(argument=argument))
        else:
            raise TypeError('expected int, tuple[int, int] or Fraction, got {type}'.format(type=type(argument)))

        if not self.validate():
            raise NoteNotSupportedError('note {note} is not supported'.format(note=self.duration))

    def __repr__(self):
        numerator, denominator, dots = self.dots
        string = "{type}{length}{dotted}".format(
            type='r' if self.pause else 'c',
            length=denominator,
            dotted='.' * dots
        )

        return string

    def validate(self) -> bool:
        numerator, denominator, dots = self.dots
        if numerator != 1:
            return False
        if denominator == 0:
            return False

        return is_power_of_two(denominator)

    @property
    def dots(self) -> (int, int, int):
        numerator = self.duration.numerator
        denominator = self.duration.denominator
        dots = 0
        while numerator % 3 == 0 and denominator % 2 == 0:
            numerator //= 3
            denominator //= 2
            dots += 1

        return numerator, denominator, dots


NoteType = Union[int, Tuple[int, int], Note]
