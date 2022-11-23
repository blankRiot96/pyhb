import os
from pathlib import Path

from colorama import Fore

from pyhb.cli.colors import OutputColors

"""Paths"""
USER_PATH = Path(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/"))
SOUNDPACKS_PATH = USER_PATH / "Soundpacks"

"""Other Constants"""
OUTPUT_COLORS = OutputColors(
    Fore.BLUE,
    Fore.CYAN,
    Fore.GREEN,
    Fore.LIGHTBLACK_EX,
    Fore.LIGHTBLUE_EX,
    Fore.LIGHTCYAN_EX,
    Fore.LIGHTGREEN_EX,
    Fore.LIGHTMAGENTA_EX,
    Fore.LIGHTRED_EX,
    Fore.LIGHTYELLOW_EX,
    Fore.MAGENTA,
    Fore.RED,
    Fore.RESET,
    Fore.YELLOW,
)
LOFI_PLAYLIST = (
    "https://www.youtube.com/playlist?list=PL6AyRhZu1p3KfZ56ToC0xZxIlpBLOsKXD"
)

"""Display Messages"""
KEYBOARD_TYPING_DISPLAY_MSG = """Playing '{sound_pack}'. 
{color}Press <ctrl + c> to exit.{reset}
""".format(
    sound_pack="{sound_pack}", color=Fore.YELLOW, reset=Fore.RESET
)
INVALID_SONG_DISPLAY_MSG = """Song '{song}' does not exist in the playlist.
For a the full list of songs see {lofi_playlist}
""".format(
    song="{song}", lofi_playlist=LOFI_PLAYLIST
)
