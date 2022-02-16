import math
from dataclasses import dataclass
from fractions import Fraction
from typing import List, Union

from rhygen.modules.exceptions import EmptyScoreException
from rhygen.modules.misc import check_type
from rhygen.modules.note import Note, NoteType
from rhygen.modules.time_signature import TimeSignatureType


@dataclass
class Phrase:
    notes: List[Note]

    def __init__(self, notes: List[NoteType] = None):
        if notes is not None:
            check_type(notes, list)
            self.notes = list(map(Note, notes))
        else:
            self.notes = []

    def __add__(self, other):
        if not isinstance(other, Phrase):
            raise TypeError('cannot add phrase to {type}'.format(type=type(other)))
        return Phrase(self.notes + other.notes)

    def __bool__(self):
        return bool(self.notes)

    def __iter__(self):
        return self.notes.__iter__()

    def __len__(self):
        return len(self.notes)

    def validate(self, time_signature: TimeSignatureType = (4, 4)) -> int:
        if not self.notes:
            raise EmptyScoreException('an empty phrase')

        total_length = 0
        checkpoints = [0]

        for note in self.notes:
            total_length += note.duration
            checkpoints.append(total_length)

        time_signature_fraction = Fraction(*time_signature)
        validation_set = {index * time_signature_fraction for index in range(
            math.ceil(total_length / time_signature_fraction) + 1)}
        checkpoints_set = set(checkpoints)
        difference = validation_set.difference(checkpoints_set)

        return int(min(difference) / time_signature_fraction) if difference else 0

    @property
    def length(self):
        return sum([note.duration for note in self.notes])

    @property
    def lcm(self):
        return math.lcm(*[note.duration.denominator for note in self.notes])


PhraseType = Union[Phrase, List[NoteType]]
