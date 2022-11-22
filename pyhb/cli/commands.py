import json
import os
import webbrowser
from typing import Optional

import click
from colorama import Fore

from pyhb.common import USER_PATH, SOUNDPACKS_PATH
from pyhb.cli.colors import OutputColorScheme
from pyhb.cli.io import list_options, get_option
from pyhb.utils import output


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def main():
    pass


def get_sound_pack() -> str:
    soundpacks = os.listdir(SOUNDPACKS_PATH)
    soundpacks.remove("config.json")

    list_options(soundpacks, OutputColorScheme.GRADIENT)
    option = get_option("Choose a soundpack: ")

    return soundpacks[option]


@main.command(help="Play keyboard sound effects")
@click.option(
    "--soundpack", "-s", is_flag=False, flag_value="", help="Choose a soundpack"
)
def start(soundpack: Optional[str]) -> None:
    """
    Start playing an ASMR `soundpack`
    To choose from existing soundpacks, try `pyhb start`

    :param soundpack:
    :return:
    """
    from pyhb.keyboard_sound_effects import play_keybrd_sfx

    if soundpack is None:
        soundpack = get_sound_pack()

    play_keybrd_sfx(soundpack)


@main.command(help="Install Soundpacks for pyhb")
def install_soundpacks() -> None:
    """
    Install all soundpacks required for `pyhb start`

    :return: None
    """
    from pyhb.install_soundpacks import install

    install(USER_PATH.__str__())


@main.command(help="Lofi music to be played")
@click.option("--song", "-s", is_flag=False, flag_value="", help="Choose a song")
def play(song: Optional[str]) -> None:
    """
    Plays a song of user's choice from YouTube
    To view full playlist visit -
    https://www.youtube.com/watch?v=EtZ2m2Zm3vY&list=PL6AyRhZu1p3KfZ56ToC0xZxIlpBLOsKXD
    or try `pyhb play`

    :param song: Song to be played
    :return: None
    """

    global COLORS
    songs = {
        "lofigirl": "https://www.youtube.com/watch?v=5qap5aO4i9A",
        "biscuit": "https://www.youtube.com/watch?v=EtZ2m2Zm3vY",
        "melancholy": "https://www.youtube.com/watch?v=RxglYGHuqFc",
        "street lights": "https://www.youtube.com/watch?v=FqXwkqfVGvA",
        "memory lane": "https://www.youtube.com/watch?v=6LXTuNDB160",
        "jiro dreams": "https://www.youtube.com/watch?v=sEYSpROMY5A",
        "*": "https://www.youtube.com/watch?v=EtZ2m2Zm3vY&list=PL6AyRhZu1p3KfZ56ToC0xZxIlpBLOsKXD",
    }

    # If song provided, play it if it exists inside of the playlist
    if song:
        if song in songs:
            webbrowser.open(songs[song])
        else:
            output(Fore.RED, f"song '{song}' does not exist in the playlist.")
            output(
                Fore.YELLOW, f"To view the full list of songs, check the playlist - "
            )
            output(
                Fore.YELLOW,
                "https://www.youtube.com/watch?v=EtZ2m2Zm3vY&list=PL6AyRhZu1p3KfZ56ToC0xZxIlpBLOsKXD",
            )
    else:
        list_options(songs, OutputColorScheme.RANDOM)

        try:
            promt = int(input("Choose a song number: "))
            webbrowser.open(list(songs.values())[promt - 1])
        except (ValueError, IndexError):
            output(Fore.RED, "Invalid entry.")


@main.command(help="Start an aesthetic typing test application")
@click.option(
    "--punctuation",
    "-p",
    flag_value=None,
    type=bool,
    help="Toggle punctuation true/false",
)
@click.option("--theme", "-t", flag_value=None, type=str, help="Choose a theme")
@click.option(
    "--duration",
    "-d",
    flag_value=None,
    type=int,
    help="Choose a duration(15 - 60 is recommended)",
)
def typetest(
    punctuation: Optional[bool], theme: Optional[str], duration: Optional[int]
) -> None:
    """
    Starts an aesthetic and simple typing test application
    Calculates WPM and Accuracy
    Has support for different themes, durations and punctuation toggle

    :param punctuation: Decides punctuation or not for the typing test
    :param theme: Decides the theme for the typing test
    :param duration: Decides the duration for the typing test
    :return: None
    """
    if os.path.exists(USER_PATH / "typing_tester/preferences.json"):
        with open(USER_PATH / "typing_tester/preferences.json") as f:
            preferences = json.load(f)
    else:
        preferences = {
            "punctuation": False,
            "theme": "lavender",
            "duration": 30,
            "last_screen_size": [770, 456],
        }
    if punctuation is not None:
        preferences["punctuation"] = punctuation
    if theme:
        preferences["theme"] = theme
    if duration:
        preferences["duration"] = duration
    with open(USER_PATH / "typing_tester/preferences.json", "w") as f:
        json.dump(preferences, f, indent=2)

    from pyhb.typing_tester import main
    from pyhb.typing_tester.display import FPS, clock, screen

    main(screen, clock, FPS)
