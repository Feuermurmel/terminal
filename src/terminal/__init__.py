import logging
import sys
from argparse import ArgumentParser
from argparse import Namespace
from collections.abc import Callable
from os import ttyname
from typing import TypeAlias

from appscript import app
from appscript import its

Color: TypeAlias = tuple[int, int, int]


class UserError(Exception):
    pass


def parse_color(value_str: str) -> Color:
    get_channel: Callable[[int], int]

    if len(value_str) == 3:
        get_channel = lambda index: int(value_str[index], 16) * 17 * 257
    elif len(value_str) == 6:
        get_channel = lambda index: int(value_str[index * 2 : index * 2 + 2], 16) * 257
    else:
        raise ValueError(f'"${value_str}" must be either 3 or 6 hex digits.')

    return get_channel(0), get_channel(1), get_channel(2)


def parse_args() -> Namespace:
    parser = ArgumentParser(
        description=(
            "Set visual attributes of the current Terminal.app tab. "
            "COLOR is either three or six hex digits to specify an RGB "
            'color, in the same way as CSS uses (without the leading "#").'
        )
    )
    parser.add_argument("--cursor", type=parse_color, metavar="COLOR")
    parser.add_argument("--background", type=parse_color, metavar="COLOR")
    parser.add_argument("--text", type=parse_color, metavar="COLOR")
    parser.add_argument("--bold-text", type=parse_color, metavar="COLOR")

    return parser.parse_args()


def main(
    cursor: Color | None,
    background: Color | None,
    text: Color | None,
    bold_text: Color | None,
) -> None:
    terminal = app("Terminal")

    try:
        tty = ttyname(sys.stdout.buffer.fileno())
    except OSError as e:
        raise UserError(f"Error getting tty name of stdout: {e}")

    # For some reason, we can't directly iterate terminal.windows.tabs:
    # "Terminal got an error: AppleEvent handler failed." number -10000
    tab = next(
        (
            tab
            for window in terminal.windows.get()
            for tab in window.tabs[its.tty == tty].get()
        ),
        None,
    )

    if tab is None:
        raise UserError(f'Tab with tty "{tty}" not found.')

    if cursor is not None:
        tab.cursor_color.set(cursor)
    if background is not None:
        tab.background_color.set(background)
    if text is not None:
        tab.normal_text_color.set(text)
    if bold_text is not None:
        tab.bold_text_color.set(bold_text)


def entry_point() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    try:
        main(**vars(parse_args()))
    except UserError as e:
        logging.error(f"error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logging.error("Operation interrupted.")
        sys.exit(130)
