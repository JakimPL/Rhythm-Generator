import os
import uuid

from IPython.core.display import Image
from abjad.persist import as_png


def create_directory() -> str:
    if not os.path.isdir('../temp'):
        os.mkdir('../temp')

    uid = uuid.uuid4()
    directory = 'temp/{uuid}'.format(uuid=uid)
    os.mkdir(directory)
    return directory


def save_score(score):
    directory = create_directory()
    path = '{directory}/score.png'.format(directory=directory)
    as_png(score, path, remove_ly=True, resolution=175)
    return format(path)


def show_score(score):
    image_path = save_score(score)
    return Image(url=image_path, unconfined=True)
