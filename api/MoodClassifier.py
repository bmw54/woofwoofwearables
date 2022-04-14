import random


def get_mood(frequency, amplitude, pitches, angles, side_bias):
    moods = ['excited','happy', 'angry', 'idle', 'alert']
    return random.choice(moods)