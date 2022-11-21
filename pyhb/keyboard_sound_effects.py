import keyboard
import os
import random
from pyhb.common import SOUNDPACKS_PATH, KEYBOARD_TYPING_DISPLAY_MSG
import typing as t

# Ignore the pygame welcome message
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import json


def load_soundpack_config() -> dict:
    """Returns the configuration for the soundpacks."""

    if not os.path.exists(SOUNDPACKS_PATH / "config.json"):
        raise FileNotFoundError(
            """
            Soundpacks config does not exist. 
            Try installing soundpacks with 'pyhb install-soundpacks'
            """
        )

    with open(SOUNDPACKS_PATH / "config.json") as f:
        config = json.load(f)

    return config["defines"]


def play_key_sfx(key: str, sound_pack: str) -> None:
    """Plays specific key stroke effect."""
    sound_obj = pygame.mixer.Sound(SOUNDPACKS_PATH / sound_pack / key)
    sound_obj.play()


def get_available_keys(sound_pack: str, config: dict) -> t.Tuple[str, t.Set[str]]:
    """Get the available keys and the file extention."""

    if sound_pack == "nk-cream":
        file_ext = ".wav"
        available_keys = {
            key.name.replace(file_ext, "")
            for key in (SOUNDPACKS_PATH / sound_pack).iterdir()
        }
    else:
        file_ext = ".ogg"
        available_keys = {
            config.get(key.name.replace(file_ext, ""))
            for key in (SOUNDPACKS_PATH / sound_pack).iterdir()
        }

    return file_ext, available_keys  # type: ignore


def play_keybrd_sfx(sound_pack: str) -> None:
    """Plays keyboard sound effects."""
    pygame.mixer.init()

    # Get available soundpacks and check if sound_pack
    # is part of it.
    available_sound_packs = os.listdir(SOUNDPACKS_PATH)
    available_sound_packs.remove("config.json")
    if sound_pack not in available_sound_packs:
        raise FileNotFoundError(
            f"""
            Soundpack '{sound_pack}' does not exist.
            """
        )

    print(KEYBOARD_TYPING_DISPLAY_MSG.format(sound_pack=sound_pack))

    config = load_soundpack_config()
    file_ext, available_keys = get_available_keys(sound_pack, config)
    registered_keys: t.Dict[str, str] = dict()

    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name is None:
                continue

            if event.name in available_keys:
                play_key_sfx(event.name + file_ext, sound_pack)
                continue

            if event.name not in registered_keys:
                registered_keys[event.name] = random.choice(tuple(available_keys))
            play_key_sfx(
                registered_keys.get(event.name, "enter") + file_ext, sound_pack
            )
