import keyboard
import os

# Ignore the pygame welcome message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame
import json

# Initialize the pygame.mixer submodule
pygame.mixer.init()

RELEASED = True

try:
    with open(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + '/Soundpacks/config.json') as f:
        config = json.load(f)
except FileNotFoundError:
    print("Soundpacks not installed, try doing 'pyhb install soundpacks'")


def set_release(*args, **kwargs):
    global RELEASED
    RELEASED = True


def main(sound_pack: str) -> None:
    """
    :param sound_pack: Name of the sound pack
    :return: None
    """
    global RELEASED
    print(f'pyhb has started playing {sound_pack}...')
    print('Use <ctrl + c> to close')
    while True:
        for key in config['defines']:
            value = config['defines'][key]
            if value is None:
                continue
            if keyboard.is_pressed(value) and RELEASED:
                if sound_pack == "nk-cream":
                    sound = pygame.mixer.Sound(f"pyhb/Soundpacks/{sound_pack}/{value}.wav")
                    sound.play()
                else:
                    sound = pygame.mixer.Sound(f"pyhb/Soundpacks/{sound_pack}/{key}.ogg")
                    sound.play()
                RELEASED = False
        keyboard.on_release(set_release)
