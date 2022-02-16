import random
from fractions import Fraction
from typing import List

import abjad

import modules.conversion
import modules.exceptions
import modules.misc
import modules.note
import modules.phrase
import modules.settings
import modules.time_signature


class RhythmGenerator:
    def __init__(self, settings: modules.settings.Settings = None):
        self.settings = settings if settings is not None else modules.settings.Settings()
        self.__cache: None

    def __call__(self) -> abjad.Score:
        self.__cache = self.__generate_score()
        return modules.conversion.to_abjad_score(self.__cache, time_signature=self.settings.time_signature)

    def __generate_measure(self, group_id: int) -> modules.phrase.Phrase:
        group_settings = self.settings.group_settings(group_id)
        phrases = group_settings.get_all_phrases()

        remainder = Fraction(*self.settings.time_signature)
        validation_message = self.__validate(phrases, remainder)
        if validation_message:
            raise modules.exceptions.InvalidPhraseSetError('invalid set of notes/phrases, {message}'.format(
                message=validation_message))

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

    def __generate_group(self, group_id: int) -> modules.phrase.Phrase:
        return sum([self.__generate_measure(group_id) for _ in range(self.settings.measures)], modules.phrase.Phrase())

    def __generate_score(self) -> List[modules.phrase.Phrase]:
        return [self.__generate_group(group_id) for group_id in range(self.settings.groups)]

    @staticmethod
    def __validate(phrases: List[modules.phrase.Phrase], remainder: Fraction) -> str:
        gcd = Fraction(
            modules.misc.gcd([phrase.length.numerator for phrase in phrases] + [remainder.numerator]),
            modules.misc.lcm([phrase.length.denominator for phrase in phrases] + [remainder.denominator])
        )

        min_length = min([phrase.length for phrase in phrases])
        if min_length > gcd:
            return 'missing notes of length {length}'.format(length=gcd)
        elif min_length > remainder:
            return 'too long notes, required a note of length {length}'.format(length=remainder)

        return ''

    @staticmethod
    def __flatten(phrases: List[modules.phrase.Phrase]) -> modules.phrase.Phrase:
        measure = modules.phrase.Phrase([])
        for phrase in phrases:
            measure.notes += phrase.notes
        return measure

    @property
    def cache(self) -> List[modules.phrase.Phrase]:
        return self.__cache
