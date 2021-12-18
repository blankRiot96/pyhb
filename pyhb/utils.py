import click
from colorama import Style


def output(color, msg) -> None:
	click.echo(color + msg + Style.RESET_ALL)

