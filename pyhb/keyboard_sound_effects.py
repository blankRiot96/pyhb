import keyboard
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame
import json

pygame.mixer.init()

RELEASED = True


with open('pyhb/Soundpacks/config.json') as f:
    config = json.load(f)


def set_release(*args, **kwargs):
    global RELEASED
    RELEASED = True


def main(sound_pack: str):
    """
    :param sound_pack: Name of the sound pack
    :return:
    """
    global RELEASED
    print(f'pyhb has started playing {sound_pack}...')
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
