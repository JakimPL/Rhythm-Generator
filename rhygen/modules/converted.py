import subprocess


def to_audio(sf2: str, midi_file: str, out_file: str, out_type: str = 'wav'):
    subprocess.call(['fluidsynth', '-T', out_type, '-F', out_file, '-ni', sf2, midi_file])
