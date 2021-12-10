import os
import sys
import webbrowser
from pyhb.table import list_info


def main():
    # Path to which 'pyhb' is installed
    user_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
    
    # Check if soundpacks are installed
    try:
        soundpacks = os.listdir(user_path + "/Soundpacks")
        soundpacks.remove('config.json')
    except FileNotFoundError:
        soundpacks = []

    commands = {
        "play": {
            "lofigirl": "https://www.youtube.com/watch?v=5qap5aO4i9A",
            "biscuit": "https://www.youtube.com/watch?v=EtZ2m2Zm3vY"
        },
        "start": ["typetest"],
        "soundpacks": soundpacks,
        "install": ["soundpacks"]
    }


    def try_index(index: int) -> str:
        try:
            value = sys.argv[index]
        except IndexError:
            value = None

        return value

    flag = try_index(1)
    optional_arg = try_index(2)

    if flag == "play":
        if optional_arg in commands[flag]:
            webbrowser.open(commands[flag][optional_arg])
        else:
            print(f"Invalid argument for the '{flag}' flag")
            list_info(list(commands["play"].keys()), list(commands["play"].values()))
    elif flag == "start":
        if optional_arg in commands[flag]:
            if optional_arg == "typetest":
                from pyhb.typing_tester import main
                main()
        else:
            print(f"Invalid argument for the '{flag}' flag")
            list_info(commands[flag])
    elif flag == "install":
        if optional_arg in commands[flag]:
            if optional_arg == "soundpacks":
                from pyhb.install_soundpacks import install
                install(os.path.dirname(os.path.realpath(__file__)))
            else:
                print(f"Invalid argument for the '{flag} flag'")
                list_info(commands[flag])
    else:
        from pyhb.keyboard_sound_effects import main

        if flag not in commands["soundpacks"]:
            print("Unavailable soundpack")
            list_info(commands["soundpacks"])
        else:
            try:
                main(flag)
            except KeyboardInterrupt:
                print("You have closed the program.")

