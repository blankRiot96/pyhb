import random as _random
import typing as _t

import click as _click
import colorama as _colorama

from pyhb.cli.colors import OutputColors, OutputColorScheme
from pyhb.common import OUTPUT_COLORS
from pyhb.utils import output


def _get_color_output(
    output: str, color_scheme: OutputColorScheme, colors: OutputColors
) -> str:
    """Gets a color output based on scheme."""
    if color_scheme == OutputColorScheme.GRADIENT:
        color = next(colors)
    elif color_scheme == OutputColorScheme.RANDOM:
        color = _random.choice(colors)

    return f"{color}{output}{_colorama.Fore.RESET}"


def list_options(
    options: _t.Iterable, color_scheme: _t.Optional[OutputColorScheme]
) -> None:
    """Lists a bunch of options."""
    for option_number, option in enumerate(options):
        output = option
        if color_scheme is not None:
            output = _get_color_output(option, color_scheme, OUTPUT_COLORS)

        _click.echo(f"[{option_number + 1}] {output}")


def get_option(prompt_msg: str, options: _t.Sequence[_t.Any]) -> _t.Any:
    """Gets one option from a list of options."""

    try:
        prompt = int(input(prompt_msg))
    except ValueError:
        output(_colorama.Fore.RED, "Please enter a number.")
        exit()

    if 0 > prompt >= len(options):
        output(_colorama.Fore.RED, "Invalid entry.")

    return options[prompt - 1]
