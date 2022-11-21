import os
from pathlib import Path


USER_PATH = Path(os.path.dirname(os.path.realpath(__file__)).replace("\\", "/"))
SOUNDPACKS_PATH = USER_PATH / "Soundpacks"


"""Display Messages"""
KEYBOARD_TYPING_DISPLAY_MSG = """Playing '{sound_pack}'. 
Press <ctrl + c> to exit.
"""
