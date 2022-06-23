from typing import List

import abjad

from rhygen.modules.exceptions import EmptyScoreException, InvalidBeatException
from rhygen.modules.phrase import Phrase
from rhygen.modules.time_signature import TimeSignatureType


def to_abjad_string(phrase: Phrase, time_signature: TimeSignatureType = (4, 4)) -> str:
    invalid_beat = phrase.validate(time_signature=time_signature)
    if invalid_beat:
        raise InvalidBeatException('invalid beat no. {beat}'.format(beat=invalid_beat))

    abjad_string = ""
    for note in phrase:
        abjad_string += '{note} '.format(note=note)
    return abjad_string


def to_abjad_score(score: List[Phrase], time_signature: TimeSignatureType = (4, 4), tempo: int = 120) -> abjad.Score:
    if not score:
        raise EmptyScoreException('an empty score')

    abjad_signature = abjad.TimeSignature(time_signature)
    abjad_tempo = abjad.MetronomeMark((1, 4), tempo)

    staves = []
    for notes in score:
        voice = abjad.Voice(to_abjad_string(notes, time_signature=time_signature), name='Rhythm')
        abjad.attach(abjad_tempo, voice[0])
        abjad.attach(abjad_signature, voice[0])
        staff = abjad.Staff([voice], lilypond_type='RhythmicStaff', name='Percussion')
        staff_group = abjad.StaffGroup([staff])
        staves.append(staff_group)

    score = abjad.Score(staves)
    return score
