import keyboard
import os
import random

# Ignore the pygame welcome message
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import json


# Initialize the pygame.mixer submodule
pygame.mixer.init()

RELEASED = True

try:
    with open(
        os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
        + "/Soundpacks/config.json"
    ) as f:
        config = json.load(f)
except FileNotFoundError:
    print("Soundpacks not installed, try doing 'pyhb install soundpacks'")


def set_release(*args, **kwargs):
    global RELEASED
    RELEASED = True


def main(sound_pack: str) -> None:
    user_path = os.path.dirname(os.path.realpath(__file__))
    """
    :param sound_pack: Name of the sound pack
    :return: None
    """
    global RELEASED
    print(f"pyhb has started playing {sound_pack}...")
    print("Use <ctrl + c> to close")

    conf_vals = list(config["defines"].values())
    conf_keys = list(config["defines"].keys())

    session = {}
    while True:
        key_pressed = keyboard.read_key()
        if key_pressed in conf_vals:
            if RELEASED:
                if sound_pack == "nk-cream":
                    sound = pygame.mixer.Sound(
                        f"{user_path}/Soundpacks/{sound_pack}/{key_pressed}.wav"
                    )
                else:
                    index = conf_vals.index(key_pressed)
                    key = conf_keys[index]
        else:
            if key_pressed not in session:
                value = conf_vals[random.randint(0, len(conf_vals) - 1)]
                session[key_pressed] = value

            key_pressed = session[key_pressed]
            index = conf_vals.index(key_pressed)
            key = conf_keys[index]

        if RELEASED:
            if sound_pack == "nk-cream":
                sound = pygame.mixer.Sound(
                    f"{user_path}/Soundpacks/{sound_pack}/{key_pressed}.wav"
                )
            else:
                sound = pygame.mixer.Sound(
                    f"{user_path}/Soundpacks/{sound_pack}/{key}.ogg"
                )
            sound.play()
            RELEASED = False

        keyboard.on_release(set_release)
