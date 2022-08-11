from pathlib import Path
from random import choices, randint
from string import ascii_uppercase, digits
from typing import List, Optional, Union

from PIL.ImageColor import getrgb
from PIL.ImageFont import truetype


def check_fonts(*fonts: Union[str, Path]) -> Optional[List[str]]:
    """Check the given fonts by loading them. If any of them fails, return their path.

    Parameters
    ----------
    fonts : :py:class:`str` or :py:class:`pathlib.Path`
        The list of fonts to check.

    Returns
    -------
    Optional, list of :py:class:`str` :
        A list of path of the non-loadable font, if any.
    """
    failures: List[str] = []
    for font in fonts:
        if isinstance(font, Path):
            font = font.absolute().as_posix()
        try:
            truetype(font)
        except OSError:
            failures.append(font)
    return failures or None


def random_color(start: int = 0, end: int = 255, opacity: int = 0) -> str:
    # sourcery skip: comprehension-to-generator, invert-any-all
    # Incorrect suggestion
    """Returns a random color in hexadecimal format.

    Parameters
    ----------
    start : Optional, :py:class:`int`
        The starting number of the color, must be contained between 0 and 255, by default 0
    end : Optional, :py:class:`int`
        The ending number of the color, must be contained between 0 and 255, by default 255
    opacity : Optional, :py:class:`int`
        The color's opacity, by default 0

    Returns
    -------
    :py:class:`str` :
        The hexadecimal color.

    Raises
    ------
    :py:exc:`ValueError` :
        If any of `start`, `end` or `opacity` is not contained between 0 and 255.
    """
    if not all([0 <= attribute <= 255 for attribute in (start, end, opacity)]):
        raise ValueError("start, end and opacity parameters must be contained between 0 and 255.")

    # Simply return a random number...
    def rc() -> int:
        return randint(start, end)

    # Convert numbers to hexadecimal
    return "#%02X%02X%02X%02X" % (rc(), rc(), rc(), opacity)


def random_code(characters_length: Optional[int] = None) -> str:
    """
    Return a random code with the needed length.

    Parameters
    ----------
    characters_length : Optional, :py:class:`int`
        The length of the returned code.

    Returns
    -------
    :py:class:`str` :
        The random code.
    """
    return "".join(choices(ascii_uppercase + digits, k=characters_length or 4))


def validate_str_to_hex(color: str) -> bool:
    """
    Validate a string to be a valid hexadecimal color.

    Parameters
    ----------
    color : :py:class:`str`:
        The string to validate.

    Returns
    -------
    :py:class:`bool` :
        If the color is hexadecimal or not.
    """
    if not color:
        # Empty string
        return False
    try:
        getrgb(color)
    except ValueError:
        return False
    return True
