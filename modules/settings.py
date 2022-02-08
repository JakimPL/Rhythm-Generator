from typing import List, Dict


class GroupSettings:
    notes: List[int] = [-8, -4, -2, 1, 2, 4, 8]
    phrases: List[List[int]] = [[4, -4], [-4, 4], [8, 8, 8, 8], [4, 4]]


class Settings:
    def __init__(self):
        self.__time_signature: (int, int) = (4, 4)
        self.__groups: int = 1
        self.__measures: int = 2
        self.__default_group_settings: GroupSettings = GroupSettings()
        self.__group_settings: Dict[int, GroupSettings] = {}

    @property
    def time_signature(self) -> (int, int):
        return self.__time_signature

    @time_signature.setter
    def time_signature(self, signature: (int, int)):
        if not (isinstance(signature, tuple) and len(signature) == 2 and all(
                [isinstance(element, int) for element in signature])):
            raise TypeError('expected a 2-tuple (int, int), got {type}'.format(type=type(signature)))

        if not all([element > 0 for element in signature]):
            raise ValueError('non-positive element in a signature: {}'.format(signature))

        self.__time_signature = signature

    @property
    def groups(self) -> int:
        return self.__groups

    @groups.setter
    def groups(self, groups: int):
        if not isinstance(groups, int):
            raise TypeError('expected int, got {type}'.format(type=type(groups)))

        if groups <= 0:
            raise ValueError('number of groups cannot be non-positive, got {value}'.format(value=groups))

        self.__groups = groups

    @property
    def measures(self) -> int:
        return self.__measures

    @measures.setter
    def measures(self, measures: int):
        if not isinstance(measures, int):
            raise TypeError('expected int, got {type}'.format(type=type(measures)))

        if measures <= 0:
            raise ValueError('number of measures cannot be non-positive, got {value}'.format(value=measures))

        self.__measures = measures
