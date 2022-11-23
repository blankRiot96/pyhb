import json
import os
import typing as _t
import webbrowser
from typing import Optional
from zipfile import ZipFile

import click
import requests

from pyhb.cli.colors import OutputColorScheme
from pyhb.cli.io import get_option, list_options
from pyhb.common import (
    INVALID_SONG_DISPLAY_MSG,
    LOFI_PLAYLIST,
    SOUNDPACKS_PATH,
    USER_PATH,
)
from pyhb.music import get_song_from_list, get_song_url, scrape_songs_from_playlist


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def main():
    pass


def get_sound_pack() -> str:
    soundpacks = os.listdir(SOUNDPACKS_PATH)
    soundpacks.remove("config.json")

    list_options(soundpacks, OutputColorScheme.GRADIENT)
    option = get_option("Choose a soundpack: ", soundpacks)

    return option


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
    from pyhb.keyboard_sfx import play_keybrd_sfx

    if soundpack is None:
        soundpack = get_sound_pack()

    play_keybrd_sfx(soundpack)


@main.command(help="Install Soundpacks for pyhb")
def install_soundpacks() -> None:
    """
    Install all soundpacks required for `pyhb start`

    :return: None
    """
    click.echo("Installing all the soundpacks now...")
    url = "https://github.com/blankRiot96/pyhb/files/7902786/Soundpacks.zip"
    r = requests.get(url, allow_redirects=True)

    with open(USER_PATH / "Soundpacks.zip", "wb") as f:
        f.write(r.content)

    file_name = USER_PATH / "Soundpacks.zip"

    # Extracting zip file
    with ZipFile(file_name, "r") as f:
        f.extractall(path=USER_PATH)
        print("Done!")

    # Removing zip file
    if os.path.exists(USER_PATH / "Soundpacks.zip"):
        os.remove(USER_PATH / "Soundpacks.zip")


@main.command(help="Lofi music to be played")
@click.option("--song", "-s", "song_title", help="Title of song to play")
def play(song_title: Optional[str]) -> None:
    """Plays a song."""

    songs = scrape_songs_from_playlist(LOFI_PLAYLIST)
    if song_title is None:
        song_url = get_song_from_list(songs)
    else:
        song_url = get_song_url(song_title, songs)

    webbrowser.open(song_url)


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
