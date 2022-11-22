import os
from pathlib import Path

from colorama import Fore

from pyhb.cli.colors import OutputColors

"""Paths"""
USER_PATH = Path(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/"))
SOUNDPACKS_PATH = USER_PATH / "Soundpacks"

"""Display Messages"""
KEYBOARD_TYPING_DISPLAY_MSG = """Playing '{sound_pack}'. 
Press <ctrl + c> to exit.
"""

"""Colors"""
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
