from typing import NamedTuple, Literal

from .utils import check_fonts as check_fonts
from .generator import CaptchaGenerator as CaptchaGenerator

class VersionInfo(NamedTuple):
    major: int
    minor: int
    patch: int
    release_level: Literal["alpha", "beta", "candidate", "final"]
    batch: int

version_info = VersionInfo(2, 0, 0, 'alpha', 0)
__version__ = f'{version_info.major}.{version_info.minor}.{version_info.patch}-{version_info.release_level}'

AVAILABLE_TYPES = ["wheezy", "image", "text"]
