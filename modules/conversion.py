import math
from typing import List, Union

import abjad

from modules.exceptions import EmptyScoreException, InvalidBeatException
from modules.misc import lcm, get_duration
from modules.note import Note


def to_note(note: int) -> Note:
    if note == 0:
        raise ValueError('a note duration must be a non-zero integer')

    return Note(duration=abs(note), pause=(note < 0))


def to_notes(score: Union[List[int], List[List[int]]]) -> List[List[Note]]:
    if not score:
        return []

    if isinstance(score[0], int):
        return [list(map(to_note, score))]
    elif isinstance(score[0], list):
        return [list(map(to_note, notes)) for notes in score]
    else:
        raise TypeError('expected int, got {type}'.format(type=type(score[0])))


def to_abjad_string(notes: List[Note]) -> str:
    invalid_beat = validate_notes(notes)
    if invalid_beat:
        raise InvalidBeatException('invalid beat no. {beat}'.format(beat=invalid_beat))
    abjad_string = ""
    for note in notes:
        abjad_string += '{type}{duration}'.format(type='r' if note.pause else 'c', duration=note.duration)
    return abjad_string


def to_abjad_score(score: Union[List[Note], List[List[Note]]], time_signature: (int, int) = (4, 4)) -> abjad.Score:
    if not score:
        raise EmptyScoreException('an empty score')

    if isinstance(score[0], Note):
        score = [score]
    elif not isinstance(score[0], list):
        raise TypeError('invalid argument, expected list[Note] or list[list[Note]], got {type}'.format(
            type=type(score[0])))

    abjad_signature = abjad.TimeSignature(time_signature)
    staves = []
    for notes in score:
        voice = abjad.Voice(to_abjad_string(notes), name='Rhythm')
        abjad.attach(abjad_signature, voice[0])
        staff = abjad.Staff([voice], lilypond_type='RhythmicStaff', name='Percussion')
        staff_group = abjad.StaffGroup([staff])
        staves.append(staff_group)

    score = abjad.Score(staves)
    return score


def validate_notes(notes: List[Union[int, Note]]) -> int:
    if not notes:
        raise EmptyScoreException('an empty note list')

    length = 0
    checkpoints = [0]

    lengths_lcm = lcm(notes)
    for note in notes:
        length += lengths_lcm // get_duration(note)
        checkpoints.append(length)

    validation_set = {lengths_lcm * index for index in range(math.ceil(max(checkpoints) / lengths_lcm) + 1)}
    checkpoints_set = set(checkpoints)
    difference = validation_set.difference(checkpoints_set)
    if difference:
        return 1 + min(difference) // lengths_lcm
    else:
        return 0
