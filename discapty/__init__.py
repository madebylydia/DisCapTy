from typing import NamedTuple, Literal

from .core import CaptchaQueue as CaptchaQueue
from .challenge import Challenge as Challenge
from .errors import *
from .utils import check_fonts as check_fonts
from .generator import (
    CaptchaGenerator as CaptchaGenerator,
    WheezyCaptcha as WheezyCaptcha,
    ImageCaptcha as ImageCaptcha,
    TextCaptcha as TextCaptcha
)

class Identifiers:
    ALPHA = 'alpha'
    BETA = 'beta'
    PRERELEASE = 'prerelease'
    FINAL = 'final'

class VersionInfo(NamedTuple):
    major: int
    minor: int
    patch: int
    release_level: Literal["alpha", "beta", "prerelease", "final"]
    batch: int

    def __str__(self) -> str:
        if self.batch:
            return f'{self.major}.{self.minor}.{self.patch}-{self.release_level}.{self.batch}'
        if self.release_level == "final":
            return f'{self.major}.{self.minor}.{self.patch}'
        else:
            return f'{self.major}.{self.minor}.{self.patch}-{self.release_level}'

version_info = VersionInfo(2, 0, 0, Identifiers.ALPHA, 0)
__version__ = str(version_info)

BUILTIN_GENERATORS = {
    "wheezy": WheezyCaptcha,
    "image": ImageCaptcha,
    "text": TextCaptcha
}
