import click
import os
import webbrowser
from colorama import Fore
from pyhb.utils import list_options, user_path
from typing import Optional


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def main():
    pass


@main.command(help="Play keyboard sound effects")
@click.option(
    "--soundpack", "-s", is_flag=False, flag_value="", help="Choose a soundpack"
)
def start(soundpack: Optional[str] = None):
    from pyhb.keyboard_sound_effects import main

    if soundpack:
        from pyhb.keyboard_sound_effects import main
    else:
        soundpacks = os.listdir(user_path + "/Soundpacks")
        soundpacks.remove("config.json")

        list_options(soundpacks, colorize=True)

        promt = int(input("Choose a soundpack: "))
        soundpack = soundpacks[promt - 1]

    main(soundpack)


@main.command(help="Install Soundpacks for pyhb")
@click.option("--soundpacks", flag_value="")
def install(soundpacks: str):
    from pyhb.install_soundpacks import install

    install(user_path)


@main.command(help="Lofi music to be played")
@click.option("--song", "-s", is_flag=False, flag_value="", help="Choose a song")
def play(song: Optional[str] = None):
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

    if song:
        webbrowser.open(songs[song])
    else:
        list_options(songs, colorize=True)

        try:
            promt = int(input("Choose a song number: "))
            webbrowser.open(list(songs.values())[promt - 1])
        except (ValueError, IndexError):
            output(Fore.RED, "Invalid entry.")


@main.command(help="Start an aesthetic typing test application")
# @click.option('--typetest', flag_value="", help="Start an aesthetic typing test application")
def typetest():
    from pyhb.typing_tester import main

    main()
