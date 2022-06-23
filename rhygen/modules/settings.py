from dataclasses import dataclass
from typing import List, Dict

from rhygen.modules.misc import check_type, is_power_of_two
from rhygen.modules.note import Note
from rhygen.modules.phrase import Phrase, PhraseType
from rhygen.modules.time_signature import TimeSignatureType


@dataclass
class GroupSettings:
    notes: List[Note]
    phrases: List[Phrase]

    def __init__(self, notes: PhraseType = None, phrases: List[PhraseType] = None):
        if notes:
            self.__notes = list(map(Note, notes))

        if phrases:
            self.__phrases = [Phrase(phrase) for phrase in phrases]

        if not self.get_all_phrases():
            raise ValueError('notes and phrases cannot be both empty')

    def get_all_phrases(self) -> List[Phrase]:
        return [Phrase([note]) for note in self.__notes] + self.__phrases

    @property
    def notes(self) -> List[Note]:
        return self.__notes

    @notes.setter
    def notes(self, notes: list):
        self.__notes = list(map(Note, notes))

    @property
    def phrases(self) -> List[Phrase]:
        return self.__phrases

    @phrases.setter
    def phrases(self, phrases: list):
        self.__phrases = list(map(Phrase, phrases))


class Settings:
    def __init__(self):
        self._time_signature: TimeSignatureType = (4, 4)
        self._tempo: int = 120
        self._groups: int = 2
        self._measures: int = 2
        self._group_settings: Dict[int, GroupSettings] = {}
        self._default_group_settings: GroupSettings = GroupSettings(
            notes=[-8, -4, -2, 2, 4, 8],
            phrases=[[4, -4], [-4, 4], [8, 8, 8, 8], [4, 4]]
        )

    def group_settings(self, group_id: int) -> GroupSettings:
        return self._group_settings[group_id] if group_id in self._group_settings else self._default_group_settings

    def set_group(self, group_id: int, group_settings: GroupSettings):
        check_type(group_settings, GroupSettings)
        self._group_settings[group_id] = group_settings

    @property
    def time_signature(self) -> TimeSignatureType:
        return self._time_signature

    @time_signature.setter
    def time_signature(self, signature: TimeSignatureType):
        if not (isinstance(signature, tuple) and len(signature) == 2 and all(
                [isinstance(element, int) for element in signature])):
            raise TypeError('expected a 2-tuple (int, int), got {type}'.format(type=type(signature)))

        if not all([element > 0 for element in signature]):
            raise ValueError('non-positive element in a signature: {}'.format(signature))

        if not is_power_of_two(signature[1]):
            raise ValueError('time signature denominator has to be a power of two')

        self._time_signature = signature

    @property
    def groups(self) -> int:
        return self._groups

    @groups.setter
    def groups(self, groups: int):
        check_type(groups, int)

        if groups <= 0:
            raise ValueError('number of groups cannot be non-positive, got {value}'.format(value=groups))

        self._groups = groups

    @property
    def measures(self) -> int:
        return self._measures

    @measures.setter
    def measures(self, measures: int):
        check_type(measures, int)

        if measures <= 0:
            raise ValueError('number of measures cannot be non-positive, got {value}'.format(value=measures))

        self._measures = measures

    @property
    def tempo(self) -> int:
        return self._tempo

    @tempo.setter
    def tempo(self, tempo: int):
        check_type(tempo, int)

        if tempo <= 0:
            raise ValueError('number of groups cannot be non-positive, got {value}'.format(value=tempo))

        self._tempo = tempo

    @property
    def default_group_settings(self) -> GroupSettings:
        return self._default_group_settings

    @default_group_settings.setter
    def default_group_settings(self, group_settings: GroupSettings):
        if not isinstance(group_settings, GroupSettings):
            raise TypeError('expected GroupSettings object, got {type}'.format(type=type(group_settings)))

        self._default_group_settings = group_settings
