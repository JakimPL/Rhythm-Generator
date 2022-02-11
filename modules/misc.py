import os
import uuid

import abjad
from IPython.core.display import Image


def is_power_of_two(value: int) -> bool:
    if value <= 0:
        return False

    while value != 1:
        if value % 2:
            return False
        value //= 2

    return True


def check_type(obj, obj_type):
    if not isinstance(obj, obj_type):
        raise TypeError('expected {}, got {}'.format(obj_type.__name__, type(obj_type)))


def create_directory() -> str:
    if not os.path.isdir('temp'):
        os.mkdir('temp')

    uid = uuid.uuid4()
    directory = 'temp/{uuid}'.format(uuid=uid)
    os.mkdir(directory)
    return directory


def save_score(score: abjad.Score, **kwargs) -> str:
    directory = create_directory()
    path = '{directory}/score.png'.format(directory=directory)
    try:
        abjad.persist.as_png(score, path, **kwargs)
    except AttributeError:
        pass

    if 'flags' in kwargs and '-dcrop' in kwargs['flags']:
        path = path[:-4] + '.cropped.png'

    return path


def show_score(score: abjad.Score, **kwargs):
    image_path = save_score(score, **kwargs)
    return Image(url=image_path, unconfined=True)
