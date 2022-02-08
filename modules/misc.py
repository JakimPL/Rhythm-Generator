import math
import os
import uuid
from typing import List, Union

from IPython.core.display import Image
from abjad.persist import as_png

from modules.note import Note
from modules.phrase_length import PhraseLength


def create_directory() -> str:
    if not os.path.isdir('../temp'):
        os.mkdir('../temp')

    uid = uuid.uuid4()
    directory = 'temp/{uuid}'.format(uuid=uid)
    os.mkdir(directory)
    return directory


def save_score(score) -> str:
    directory = create_directory()
    path = '{directory}/score.png'.format(directory=directory)
    as_png(score, path, remove_ly=True, resolution=175)
    return path


def show_score(score):
    image_path = save_score(score)
    return Image(url=image_path, unconfined=True)


def get_duration(note: Union[int, Note]):
    if isinstance(note, int):
        return abs(note)
    elif isinstance(note, Note):
        return note.duration
    else:
        raise TypeError('expected int or Note, got {type}'.format(type=type(note)))


def get_length(notes: List[Union[int, Note]]) -> PhraseLength:
    lengths_lcm = lcm(notes)
    length = sum([lengths_lcm // get_duration(note) for note in notes])
    return PhraseLength(lengths_lcm, length)


def lcm(notes: List[Union[int, Note]]) -> int:
    return math.lcm(*[get_duration(note) for note in notes])
