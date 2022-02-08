import math
import random
from typing import List

import abjad

from modules.conversion import to_notes, to_abjad_score
from modules.misc import get_length, flatten
from modules.settings import Settings


class RhythmGenerator:
    def __init__(self):
        self.settings: Settings = Settings()
        self.__cache: List[List[int]] = []

    def __call__(self) -> abjad.Score:
        self.__cache = self.__generate_score()
        score = to_notes(self.__cache)
        return to_abjad_score(score, time_signature=self.settings.time_signature)

    def __notes_with_lengths(self, group_id: int) -> (int, List[int], List[List[int]]):
        group_settings = self.settings.group_settings(group_id)
        notes_lcm = math.lcm(*list(map(abs, group_settings.notes)))
        phrases_lengths = list(map(get_length, group_settings.phrases))
        phrases_lcm = math.lcm(*[phrase_length.lcm for phrase_length in phrases_lengths])

        lcm = math.lcm(notes_lcm, phrases_lcm)
        notes = [lcm // note for note in group_settings.notes]
        phrases = [[lcm // note for note in phrase] for phrase in group_settings.phrases]
        return lcm, notes, phrases

    def __generate_measure(self, group_id: int) -> List[int]:
        lcm, notes, phrases = self.__notes_with_lengths(group_id)

        length = 0
        remainder = lcm
        elements = []
        while remainder:
            possible_phrases = [phrase for phrase in phrases if sum(list(map(abs, phrase))) <= remainder]
            possible_notes = [note for note in notes if abs(note) <= remainder]

            choice = random.choice(possible_phrases + possible_notes)
            if isinstance(choice, int):
                length += abs(choice)
                elements.append(lcm // choice)
            elif isinstance(choice, list):
                length += sum(list(map(abs, choice)))
                elements.append([lcm // note for note in choice])
            else:
                raise TypeError('expected int or list[int], got {type}'.format(type=type(choice)))

            remainder = lcm - length

        random.shuffle(elements)
        measure = flatten(elements)
        return measure

    def __generate_group(self, group_id: int) -> List[int]:
        return sum([self.__generate_measure(group_id) for _ in range(self.settings.measures)], [])

    def __generate_score(self) -> List[List[int]]:
        return [self.__generate_group(group_id) for group_id in range(self.settings.groups)]

    @property
    def cache(self) -> List[List[int]]:
        return self.__cache
