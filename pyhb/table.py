from typing import List

# TODO: Make a better way to do this 
def list_info(options: List[str], other_options: List[str] = None) -> None:
    print("Available options: ")
    if other_options:
        output = ""
        for option, other_option in zip(options, other_options):
            output += f"- {option}\t{other_option}\n"
        print(output)
    else:
        for option in options:
            print(f"- {option}")
