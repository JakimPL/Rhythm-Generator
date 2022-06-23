import os
import pathlib
from typing import Union

import abjad
import pydub
from rhygen.modules.converted import to_audio

SOUNDFONT = 'st_concert.sf2'
AUDIO_FORMAT = 'wav'
CONVERT_TO_MP3 = True


class Exporter:
    def __init__(self, sf2: str = SOUNDFONT, audio_format: str = AUDIO_FORMAT, convert_to_mp3: bool = CONVERT_TO_MP3):
        self.soundfont_path = os.path.join(os.getcwd(), 'soundfont', sf2)
        self.audio_format = audio_format
        self.convert_to_mp3 = convert_to_mp3

    @staticmethod
    def prepare_ly_file(score: abjad.Score) -> abjad.LilyPondFile:
        score_block = abjad.Block('score', items=[score])
        midi_block = abjad.Block('midi')
        score_block.items.append(midi_block)
        return abjad.LilyPondFile([score_block])

    @staticmethod
    def export_score(score: Union[abjad.Score, abjad.LilyPondFile], directory: str = None, **kwargs) -> str:
        if directory is None:
            directory = os.getcwd()

        original_path = os.path.join(directory, 'score_uncropped.png')
        path = os.path.join(directory, 'score.png')

        try:
            abjad.persist.as_png(score, original_path, remove_ly=True, resolution=250, flags='--png -dcrop', **kwargs)
        except AttributeError:
            pass

        cropped_path = original_path[:-4] + '.cropped.png'
        os.rename(cropped_path, path)

        return path

    @staticmethod
    def export_midi(score: Union[abjad.Score, abjad.LilyPondFile], directory: str = None, **kwargs) -> str:
        if directory is None:
            directory = os.getcwd()

        original_path = os.path.join(directory, 'score.midi')
        path = str(pathlib.Path(original_path).with_suffix('.mid'))

        ly_file = Exporter.prepare_ly_file(score) if isinstance(score, abjad.Score) else score
        abjad.persist.as_midi(ly_file, original_path, remove_ly=False, **kwargs)

        os.rename(original_path, path)

        return path

    def export_audio(self, midi_path: str, audio_path: str) -> str:
        to_audio(self.soundfont_path, midi_path, audio_path, out_type=self.audio_format)
        if self.convert_to_mp3:
            mp3_path = str(pathlib.Path(audio_path).with_suffix('.mp3'))
            sound = pydub.AudioSegment.from_wav(audio_path)
            sound.export(mp3_path, format='mp3')
            return mp3_path
        else:
            return audio_path

    @staticmethod
    def show_score(score: abjad.Score, **kwargs):
        from IPython.core.display import Image
        image_path = Exporter.export_score(score, **kwargs)
        return Image(url=image_path, unconfined=True)

    def export(self, score: abjad.Score, directory: str):
        if not isinstance(score, abjad.Score):
            raise TypeError('expected abjad.Score, got {type}'.format(type=type(score)))

        image_path = self.export_score(score, directory)
        midi_path = self.export_midi(score, directory)
        audio_path = os.path.join(directory, 'score.wav')
        mp3_path = self.export_audio(midi_path, audio_path)

        return image_path, midi_path, mp3_path
