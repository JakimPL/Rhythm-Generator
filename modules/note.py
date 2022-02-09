from dataclasses import dataclass
from fractions import Fraction
from typing import Tuple, Union


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

    def __repr__(self):
        # partially implemented
        return "{type}{length}".format(type='r' if self.pause else 'c', length=self.duration.denominator)


NoteType = Union[int, Tuple[int, int], Note]
