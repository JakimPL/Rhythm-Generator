import random
from fractions import Fraction
from typing import List, Optional

import abjad

from rhygen.modules import misc
from rhygen.modules.conversion import to_abjad_score
from rhygen.modules.exceptions import InvalidPhraseSetError
from rhygen.modules.phrase import Phrase
from rhygen.modules.settings import Settings


class RhythmGenerator:
    def __init__(self, settings: Settings = None):
        self.settings = settings if settings is not None else Settings()
        self._cache: Optional[List[Phrase]] = None

    def __call__(self) -> abjad.Score:
        self._cache = self._generate_score()
        return to_abjad_score(
            self._cache,
            time_signature=self.settings.time_signature,
            tempo=self.settings.tempo
        )

    def _generate_measure(self, group_id: int) -> Phrase:
        group_settings = self.settings.group_settings(group_id)
        phrases = group_settings.get_all_phrases()

        remainder = Fraction(*self.settings.time_signature)
        validation_message = self._validate(phrases, remainder)
        if validation_message:
            raise InvalidPhraseSetError('invalid set of notes/phrases, {message}'.format(
                message=validation_message))

        elements = []
        while remainder:
            possible_phrases = [phrase for phrase in phrases if phrase.length <= remainder]
            choice = random.choice(possible_phrases)
            elements.append(choice)
            length = choice.length
            remainder -= length

        random.shuffle(elements)
        measure = self._flatten(elements)
        return measure

    def _generate_group(self, group_id: int) -> Phrase:
        return sum([self._generate_measure(group_id) for _ in range(self.settings.measures)], Phrase())

    def _generate_score(self) -> List[Phrase]:
        return [self._generate_group(group_id) for group_id in range(self.settings.groups)]

    @staticmethod
    def _validate(phrases: List[Phrase], remainder: Fraction) -> str:
        gcd = Fraction(
            misc.gcd([phrase.length.numerator for phrase in phrases] + [remainder.numerator]),
            misc.lcm([phrase.length.denominator for phrase in phrases] + [remainder.denominator])
        )

        min_length = min([phrase.length for phrase in phrases])
        if min_length > gcd:
            return 'missing notes of length {length}'.format(length=gcd)
        elif min_length > remainder:
            return 'too long notes, required a note of length {length}'.format(length=remainder)

        return ''

    @staticmethod
    def _flatten(phrases: List[Phrase]) -> Phrase:
        measure = Phrase([])
        for phrase in phrases:
            measure.notes += phrase.notes
        return measure

    @property
    def cache(self) -> List[Phrase]:
        return self._cache
