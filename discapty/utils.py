from random import SystemRandom, randint
from string import ascii_uppercase, digits

from PIL.ImageColor import getrgb

ESCAPE_CHAR = "\u200B"
table = [i * 1.97 for i in range(256)]


def random_code(length: int = 8):
    return "".join(
        SystemRandom().choice(ascii_uppercase + digits) for _ in range(length)
    )


def random_color(start: int = 0, end: int = 255, opacity: int = 0):
    if not all([0 <= attribute <= 255 for attribute in (start, end, opacity)]):
        raise ValueError(
            "start, end and opacity parameters must be contained between 0 and 255."
        )

    def color():
        return randint(start, end)

    return "#%02X%02X%02X%02X" % (color(), color(), color(), opacity)


def validate_color(color: str) -> bool:
    if not color:
        return False
    try:
        getrgb(color)
    except ValueError:
        return False
    return True
