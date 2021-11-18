import sys

commands = {
    "-play": [""],
    "-start": ["typetest"]
}

flag = sys.argv[1]
optional_arg = sys.argv[2]

if flag == "-start":
    if optional_arg in commands[sys.argv[1]]:
        if optional_arg == "typetest":
            import pyhb.typing_tester
    else:
        print("Invalid optional argument for the '-start' flag")
        print(f"Available options: {commands['-start']}")
