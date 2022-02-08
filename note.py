from dataclasses import dataclass


@dataclass
class Note:
    duration: int
    pause: bool = False
