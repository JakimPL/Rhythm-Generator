from dataclasses import dataclass


@dataclass
class PhraseLength:
    lcm: int
    length: int

    def __repr__(self):
        return "{} of 1 / {} ({})".format(self.length, self.lcm, self.real_length)

    @property
    def real_length(self) -> float:
        return self.length / self.lcm
