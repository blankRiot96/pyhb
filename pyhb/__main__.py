import sys
import webbrowser
from pyhb.table import list_info

commands = {
    "play": {
        "lofigirl": "https://www.youtube.com/watch?v=5qap5aO4i9A",
    },
    "start": ["typetest"],
    "soundpacks": [
        "cherrymx-black-abs",
        "cherrymx-black-pbt",
        "cherrymx-blue-abs",
        "cherrymx-blue-pbt",
        "cherrymx-brown-abs",
        "cherrymx-brown-pbt",
        "cherrymx-red-abs",
        "cherrymx-red-pbt",
        "nk-cream",
        "topre-purple-hybrid-pbt"
    ]
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
else:
    from pyhb.keyboard_sound_effects import main

    if flag not in commands["soundpacks"]:
        print("Unavailable soundpack")
        list_info(commands["soundpacks"])
    else:
        main(flag)
