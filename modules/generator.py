import random
from typing import List

import abjad

from modules.conversion import to_abjad_score
from modules.phrase import Phrase
from modules.settings import Settings


class RhythmGenerator:
    def __init__(self):
        self.settings: Settings = Settings()
        self.__cache: []

    def __call__(self) -> abjad.Score:
        self.__cache = self.__generate_score()
        return to_abjad_score(self.__cache, time_signature=self.settings.time_signature)

    def __generate_measure(self, group_id: int) -> Phrase:
        group_settings = self.settings.group_settings(group_id)
        phrases = group_settings.get_all_phrases()

        remainder = 1
        elements = []
        while remainder:
            possible_phrases = [phrase for phrase in phrases if phrase.length <= remainder]
            choice = random.choice(possible_phrases)
            elements.append(choice)
            length = choice.length
            remainder -= length

        random.shuffle(elements)
        measure = self.__flatten(elements)
        return measure

    def __generate_group(self, group_id: int) -> Phrase:
        return sum([self.__generate_measure(group_id) for _ in range(self.settings.measures)], Phrase())

    def __generate_score(self) -> List[Phrase]:
        return [self.__generate_group(group_id) for group_id in range(self.settings.groups)]

    @staticmethod
    def __flatten(phrases: List[Phrase]) -> Phrase:
        measure = Phrase([])
        for phrase in phrases:
            measure.notes += phrase.notes
        return measure

    @property
    def cache(self) -> List[Phrase]:
        return self.__cache
