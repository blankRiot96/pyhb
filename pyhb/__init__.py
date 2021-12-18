import click
import os
import webbrowser
import random
from colorama import Fore, Style, Back
from pyhb.utils import output


COLORS = [
	Fore.BLACK,
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
	Fore.YELLOW
]


@click.group()
@click.option('--play', is_flag=True, flag_value="", help="Lofi music to be played")
@click.option('--typetest', flag_value="", help="Start an aesthetic typing test application")
def cli():
	pass


@cli.command()
def play_song(play):
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

	if play:
		webbrowser.open(songs[play])
	else:
		for index, song in enumerate(songs):
			color = random.choice(COLORS)
			output(color, f"[{index + 1}] {song}")

		try:
			promt = int(input('Choose a song number: '))
			webbrowser.open(list(songs.values())[promt - 1])
		except (ValueError, IndexError):
			output(Fore.RED, "Invalid entry.")


@cli.command()
def type_test():
	from pyhb.typing_tester import main 
	main()


def main():
	cli()
