"""
Utility file for pyhb
Contains commonly used functions and variables used across the project
"""

import click
from colorama import Fore, Style


def output(color: str, msg: str) -> None:
    """
    Outputs message and resets terminal color back to default

    :param color: Color to output
    :param msg: Message to output
    :return: None
    """
    click.echo(color + msg + Style.RESET_ALL)
