#  Copyright (c) 2022​-present - Predeactor - Licensed under the MIT License.
#  See the LICENSE file included with the file for more information about this project's
#   license.

import pathlib
import typing
from abc import ABCMeta, abstractmethod
from os import listdir
from os.path import abspath, dirname, isfile, join
from random import choice, randint, random, uniform

import PIL.Image
import PIL.ImageColor
import PIL.ImageDraw
import PIL.ImageFilter
import PIL.ImageFont
import pydantic
from pydantic.color import Color

from discapty.utils import random_color

from .wheezylib import image as wheezy_captcha

PATH = join(abspath(dirname(__file__)), "fonts")
DEFAULT_FONTS = [join(PATH, f) for f in listdir(PATH) if isfile(join(PATH, f))]


class Generator(pydantic.BaseModel, metaclass=ABCMeta):
    """
    Base class for all generators.

    A generator is used to especially generate a Captcha object based on a given text.
    A generator looks like this:

    .. code-block:: python

       class MyGenerator(Generator):
           def generate(self, text: str) -> str:
               return "+".join(text)


    A generator can be supplied with parameters using class's attributes, for example:


    .. code-block:: python

       class MyGenerator(Generator):
           separator = "+"

           def generate(self, text: str) -> str:
               return self.separator.join(text)

       gen1 = MyGenerator()  # Separator here is "+"
       gen2 = MyGenerator(separator="-")  # Separator here is "-"


    Here, separator has a default value, which can be overridden by the user, or not.
    If you wish to create a generator with a required value, you can use "...", like this:


    .. code-block:: python

       class MyGenerator(Generator):
           separator: str = ...

           ...

       MyGenerator(separator="+")  # Works! 👍
       MyGenerator()  # Raises an error! 👎


    If you wish to know more on that subject, visit Pydantic's documentation as this is what
    :py:obj:`Generator` uses under the hood.
    https://pydantic-docs.helpmanual.io/

    .. versionadded:: 2.0.0
    """

    class Config:
        validate_all = True
        validate_assignment = True

    @property
    def required_keys(self) -> typing.List[str]:
        """
        Returns a list of all child's required keys.
        """
        return [key for key, value in self.__fields__.items() if value.required]

    @property
    def optional_keys(self) -> typing.List[str]:
        """
        Returns a list of all child's optional keys.
        """
        return [key for key, value in self.__fields__.items() if not value.required]

    @abstractmethod
    def generate(self, text: str) -> typing.Any:
        """
        A method that needs to be implemented by the child class.
        This method will return the Captcha that the user has requested. See class's docstring.
        """
        raise NotImplementedError()


class WheezyGenerator(Generator):
    """
    A wheezy image Captcha generator. Comes with many customizable settings.
    Easier to read than Image.

    Example: https://imgur.com/a/l9V09PN
    """

    fonts: typing.Sequence[typing.Union[pydantic.FilePath, str]] = DEFAULT_FONTS
    fonts_size: typing.Tuple[int, ...] = (50,)
    width: int = 300
    height: int = 125
    background_color: Color = "#EEEECC"
    text_color: Color = "#5C87B2"
    text_squeeze_factor: float = 0.8
    noise_number: int = 30
    noise_color: Color = "#EEEECC"
    noise_level: int = 2

    @pydantic.validator("fonts_size")
    def as_many_size_as_fonts(
        cls, v: typing.Tuple[int, ...], values: typing.Dict[str, typing.Any]
    ):
        if "fonts" in values and len(v) != len(values["fonts"]):
            raise ValueError("The number of fonts_size must be equal to the number of fonts")
        return v

    def generate(self, text: str) -> PIL.Image.Image:
        """
        Generate a wheezy image. See https://imgur.com/a/l9V09PN.
        """
        fonts: typing.List[str] = [
            font if isinstance(font, str) else font.absolute().as_posix() for font in self.fonts
        ]

        fn = wheezy_captcha.captcha(
            drawings=[
                wheezy_captcha.background(self.background_color.as_hex()),
                wheezy_captcha.text(
                    fonts=fonts,
                    fonts_sizes=self.fonts_size,
                    drawings=[
                        wheezy_captcha.warp(),
                        wheezy_captcha.rotate(),
                        wheezy_captcha.offset(),
                    ],
                    text_color=self.text_color.as_hex(),
                    squeeze_factor=self.text_squeeze_factor,
                ),
                wheezy_captcha.curve(),
                wheezy_captcha.noise(
                    noise_number=self.noise_number,
                    noise_color=self.noise_color.as_hex(),
                    noise_width=self.noise_level,
                ),
                wheezy_captcha.smooth(),
            ],
            width=self.width,
            height=self.height,
        )
        return fn(text)


class ImageGenerator(Generator):
    """
    An image Captcha generator. Comes with many customizable settings.
    More harder than the Wheezy generator.

    Example: https://imgur.com/a/wozYgW0
    """

    fonts: typing.Sequence[typing.Union[pydantic.FilePath, str]] = DEFAULT_FONTS
    fonts_size: typing.Tuple[int, ...] = (50,)

    background_color: Color = pydantic.Field(random_color(238, 255))
    text_color: Color = pydantic.Field(random_color(10, 200, 100))
    number_of_dots: int = 100
    width_of_dots: int = 3
    number_of_curves: int = 1
    width: int = 300
    height: int = 125

    def get_truefonts(self) -> typing.Tuple[PIL.ImageFont.FreeTypeFont, ...]:
        return self._fetch_truefonts(list(self.fonts), self.fonts_size)

    @staticmethod
    def _fetch_truefonts(
        fonts: typing.Sequence[typing.Union[pydantic.FilePath, str]],
        fonts_sizes: typing.Tuple[int, ...],
    ) -> typing.Tuple[PIL.ImageFont.FreeTypeFont, ...]:
        return tuple(
            PIL.ImageFont.truetype(n, s)
            for n in [f.absolute().as_posix() if isinstance(f, pathlib.Path) else f for f in fonts]
            for s in fonts_sizes
        )

    @staticmethod
    def create_noise_curve(
        image: PIL.Image.Image, color: Color, number: int = 1
    ) -> PIL.Image.Image:
        w, h = image.size
        while number:
            x1 = randint(0, int(w / 5))
            x2 = randint(w - int(w / 5), w)
            y1 = randint(int(h / 5), h - int(h / 5))
            y2 = randint(y1, h - int(h / 5))
            points = [x1, y1, x2, y2]
            end = randint(160, 200)
            start = randint(0, 20)
            PIL.ImageDraw.Draw(image).arc(
                points, start, end, fill=PIL.ImageColor.getrgb(color.as_hex())
            )
            number -= 1
        return image

    @staticmethod
    def create_noise_dots(
        image: PIL.Image.Image, color: Color, width: int = 3, number: int = 30
    ) -> PIL.Image.Image:
        draw = PIL.ImageDraw.Draw(image)
        w, h = image.size
        while number:
            x1 = randint(0, w)
            y1 = randint(0, h)
            pos = ((x1, y1), (x1 - 1, y1 - 1))
            draw.line(pos, fill=PIL.ImageColor.getrgb(color.as_hex()), width=width)
            number -= 1
        return image

    def create_captcha_image(self, *, chars: str) -> PIL.Image.Image:
        image = PIL.Image.new(
            "RGB",
            (self.width, self.height),
            PIL.ImageColor.getrgb(self.background_color.as_hex()),
        )
        draw = PIL.ImageDraw.Draw(image)

        def _draw_character(char: str) -> PIL.Image.Image:
            font = choice(self.get_truefonts())
            wid, hei = draw.textsize(char, font=font)

            dx = randint(0, 4)
            dy = randint(0, 6)
            im = PIL.Image.new("RGBA", (wid + dx, hei + dy))
            PIL.ImageDraw.Draw(im).text(  # type: ignore
                (dx, dy),
                char,
                font=font,
                fill=PIL.ImageColor.getrgb(self.text_color.as_hex()),
            )

            # Rotate
            im = im.crop(im.getbbox())
            im = im.rotate(uniform(-30, 30), PIL.Image.BILINEAR, expand=True)

            # Warp
            dx = wid * uniform(0.1, 0.3)
            dy = hei * uniform(0.2, 0.3)
            x1 = int(uniform(-dx, dx))
            y1 = int(uniform(-dy, dy))
            x2 = int(uniform(-dx, dx))
            y2 = int(uniform(-dy, dy))
            w2 = wid + abs(x1) + abs(x2)
            h2 = hei + abs(y1) + abs(y2)
            data = (
                x1,
                y1,
                -x1,
                h2 - y2,
                w2 + x2,
                h2 + y2,
                w2 - x2,
                -y1,
            )
            im = im.resize((w2, h2))
            im = im.transform((wid, hei), PIL.Image.QUAD, data)
            return im

        images: typing.List[PIL.Image.Image] = []

        for c in chars:
            if random() > 0.5:
                images.append(_draw_character(" "))
            images.append(_draw_character(c))

        text_width = sum([im.size[0] for im in images])

        width = max(text_width, self.width)
        image = image.resize((width, self.height))

        average = int(text_width / len(chars))
        rand = int(0.25 * average)
        offset = int(average * 0.1)

        for im in images:
            w, h = im.size
            mask = im.convert("L").point([int(i * 1.97) for i in range(256)])  # type: ignore
            image.paste(im, (offset, int((self.height - h) / 2)), mask)
            offset = offset + w + randint(-rand, 0)

        image = image.resize((width, self.height))

        return image

    def generate(self, text: str) -> PIL.Image.Image:
        """Generate a Captcha image. See x"""
        im = self.create_captcha_image(chars=text)
        self.create_noise_dots(im, self.text_color, self.width_of_dots, self.number_of_dots)
        self.create_noise_curve(im, self.text_color, self.number_of_curves)
        im = im.filter(PIL.ImageFilter.SMOOTH)
        return im


class TextGenerator(Generator):
    """
    A text-based Captcha generator.
    Most insecure, but it is the most tricky.

    It adds a specific separator between each character of the given text.
    The default separator is an invisible space. (\\\\u200B)
    """

    separator: typing.Union[str, typing.List[str]] = "\u200B"

    def generate(self, text: str) -> str:
        if isinstance(self.separator, str):
            return self.separator.join(text)
        new_string: str = ""
        for position, character in enumerate(text):
            char = choice(self.separator)
            new_string += character + (char if position < len(text) - 1 else "")
        return new_string
