from PIL.ImageFont import truetype
from typing import List, Optional, Union
from pathlib import Path


def check_fonts(*fonts: Union[str, Path]) -> Optional[List[str]]:
    """Check the given fonts by loading them. If any of them fails, return their path.

    Returns
    -------
    List[str] - Optional
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
    if failures:
        return failures
    # NoReturn
