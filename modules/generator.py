from typing import List

from modules.settings import Settings


class RhythmGenerator:
    def __init__(self):
        self.settings: Settings = Settings()
        self.__cache: List[List[int]] = []

    def __call__(self) -> List[List[int]]:
        self.__cache = self.__generate_score()
        return self.cache

    def __generate_measure(self, group_id: int) -> List[int]:
        pass

    def __generate_group(self, group_id: int) -> List[int]:
        return sum([self.__generate_measure(group_id) for _ in range(self.settings.measures)])

    def __generate_score(self) -> List[List[int]]:
        return [self.__generate_group(group_id) for group_id in range(self.settings.groups)]

    @property
    def cache(self) -> List[List[int]]:
        return self.__cache
