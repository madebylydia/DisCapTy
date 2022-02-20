from abc import ABCMeta, abstractmethod
from os import listdir
from os.path import abspath, dirname, isfile, join

from pathlib import Path
from typing import Any, List, Union

from .errors import InvalidFont
from .utils import check_fonts


path = join(abspath(dirname(__file__)), "fonts")
DEFAULT_FONTS = [join(path, f) for f in listdir(path) if isfile(join(path, f))]

class CaptchaGenerator(metaclass=ABCMeta):
    """The base generator that takes care of creating a sane base for all generator.

    It permits an easier implementation of a custom captcha's generator as such:

    .. code-block :: python

        from discapty import CaptchaGenerator

        class MyCustomGenerator(CaptchaGenerator):
            def generate(self):
                return generate_captcha_code()

    .. tip ::
    
        DisCapTy already include 3 differents generator: Wheezy, Image and Text. Check
        them out before rewritting the wheel!
    """
    def __init__(self) -> None:
        self.name: str

        self._fonts: List[Path] = []

    @property
    def fonts(self) -> List[Path]:
        """Get the fonts.

        Returns
        -------
        List[Path]
            The list of font's paths.
        """
        return self._fonts

    @fonts.setter
    def fonts(self, *fonts: Union[str, Path]) -> None:
        """Set the font to use for the generator.

        Raises
        ------
        InvalidFont
            If any of the given fonts is invalid, raise this error.
        """
        if failures := check_fonts(*fonts):
            if len(failures) > 1:
                raise InvalidFont(f"The following fonts path are invalid: {failures}")
            else:
                raise InvalidFont(f'This font path is not valid: {failures[0]}')
        self._fonts = [
            Path(font) if isinstance(font, str) else font for font in fonts
        ]

    @abstractmethod
    def generate(self) -> Any:
        """
        Generate the image.
        """
        raise NotImplementedError()

class WheezyCaptcha(CaptchaGenerator):
    pass

class ImageCaptcha(CaptchaGenerator):
    pass

class TextCaptcha(CaptchaGenerator):
    pass
