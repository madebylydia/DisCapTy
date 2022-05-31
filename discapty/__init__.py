import typing
from typing import Literal, NamedTuple, Optional

from pydantic.color import Color as Color

from .challenge import Challenge as Challenge
from .core import CaptchaQueue as CaptchaQueue
from .errors import *
from .generators import ImageGenerator as ImageGenerator
from .generators import TextGenerator as TextGenerator
from .generators import WheezyGenerator as WheezyGenerator


class Identifiers:
    ALPHA = "alpha"
    BETA = "beta"
    FINAL = "final"


class VersionInfo(NamedTuple):
    major: int
    minor: int
    patch: int
    release_level: Literal["alpha", "beta", "final"]
    batch: Optional[int]

    def __str__(self) -> str:
        if self.batch:
            return (
                f"{self.major}.{self.minor}.{self.patch}-{self.release_level}."
                f"{self.batch}"
            )
        if self.release_level == "final":
            return f"{self.major}.{self.minor}.{self.patch}"
        else:
            return f"{self.major}.{self.minor}.{self.patch}-{self.release_level}"

    def to_tuple(
        self,
    ) -> typing.Tuple[int, int, int, Literal["alpha", "beta", "final"], Optional[int]]:
        """
        Export version string as tuple.
        """
        return (self.major, self.minor, self.patch, self.release_level, self.batch)


version_info = VersionInfo(2, 0, 0, Identifiers.ALPHA, 1)
__version__ = str(version_info)
