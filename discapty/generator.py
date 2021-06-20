# Please read the last line of the license for more informations about this code.


import random
from os import PathLike, listdir
from os.path import abspath, dirname, isfile, join
from typing import List, Optional, Tuple, Union

import PIL
from wheezy.captcha import image as wheezy_captcha

from .typehint import CaptchaGen
from .utils import ESCAPE_CHAR, table

path = join(abspath(dirname(__file__)), "fonts")
DEFAULT_FONTS = [join(path, f) for f in listdir(path) if isfile(join(path, f))]


class WheezyCaptcha(CaptchaGen):
    """Create an image CAPTCHA with wheezy.captcha."""

    def __init__(self, *, fonts: List[Union[PathLike, str]]):
        super().__init__(fonts=fonts)
        self.fonts: List[Union[PathLike, str]] = fonts or DEFAULT_FONTS

    def generate(
        self,
        chars: str,
        *,
        width: Optional[int] = 200,
        height: Optional[int] = 75,
        font_sizes: Optional[Tuple[int]] = None
    ):
        fn: PIL.Image = wheezy_captcha.captcha(
            drawings=[
                wheezy_captcha.background(),
                wheezy_captcha.text(
                    fonts=self.fonts,
                    font_sizes=font_sizes,
                    drawings=[
                        wheezy_captcha.warp(),
                        wheezy_captcha.rotate(),
                        wheezy_captcha.offset(),
                    ],
                ),
                wheezy_captcha.curve(),
                wheezy_captcha.noise(),
                wheezy_captcha.smooth(),
            ],
            width=width,
            height=height,
        )
        return fn(chars)


class ImageCaptcha(CaptchaGen):
    """Create an image CAPTCHA.

    Many of the codes are borrowed from wheezy.captcha, with a modification for memory and
    developer friendly.

    ImageCaptcha has one built-in font, Roboto Regular, which is licensed under Apache
    License 2. You can use your own fonts:
        captcha = ImageCaptcha(fonts=['/path/to/A.ttf', '/path/to/B.ttf'])
    You can put as many fonts as you like. But be aware of your memory, all of
    the fonts are loaded into your memory, so keep them a lot, but not too
    many.
    """

    def __init__(
        self,
        *,
        fonts: Optional[List[Union[PathLike, str]]],
        fonts_size: Optional[Tuple[int]]
    ):
        super().__init__(fonts=fonts)
        self.fonts: List[Union[PathLike, str]] = fonts or DEFAULT_FONTS
        self.font_sizes: Tuple[int] = fonts_size or (50,)
        self.__truefonts: Tuple[PIL.ImageFont.FreeTypeFont] = self.fetch_truefonts(
            self.fonts, self.font_sizes
        )

    def get_truefonts(self):
        return self.__truefonts

    @staticmethod
    def fetch_truefonts(font: List[Union[PathLike, str]], font_sizes: Tuple[int]):
        return tuple(PIL.ImageFont.truetype(n, s) for n in font for s in font_sizes)

    @staticmethod
    def create_noise_curve(image: PIL.Image, color: Tuple[int, int, int]):
        w, h = image.size
        x1 = random.randint(0, int(w / 5))
        x2 = random.randint(w - int(w / 5), w)
        y1 = random.randint(int(h / 5), h - int(h / 5))
        y2 = random.randint(y1, h - int(h / 5))
        points = [x1, y1, x2, y2]
        end = random.randint(160, 200)
        start = random.randint(0, 20)
        PIL.ImageDraw.Draw(image).arc(points, start, end, fill=color)
        return image

    @staticmethod
    def create_noise_dots(
        image: PIL.Image, color: Tuple[int, int, int], width: int = 3, number: int = 30
    ):
        draw = PIL.ImageDraw.Draw(image)
        w, h = image.size
        while number:
            x1 = random.randint(0, w)
            y1 = random.randint(0, h)
            pos = ((x1, y1), (x1 - 1, y1 - 1))
            draw.line(pos, fill=color, width=width)
            number -= 1
        return image

    def create_captcha_image(
        self,
        chars: str,
        *,
        color: Tuple[int, int, int],
        background: Tuple[int, int, int, int],
        width: int,
        height: int
    ) -> PIL.Image:
        """Generate a CAPTCHA image.

        Parameters
        ----------
        chars: str
            The captcha's text to be generated.
        color: Tuple[int, int, int]
            The captcha's text color that will be generated. The tuple will contains
            a set of integrer that represent red, green and blue (RGB). Must be
            contained between 0 and 255.
        background: Tuple[int, int, int, int]
            The captcha's background color that will be generated. The tuple will contains
            a set of integrer that represent red, green and blue and transparence
            (RGB + transparence). Must be contained between 0 and 255. Last integrer represent
            the opacity of the color.
        width: int
            The width of the generated image.
        height: int
            The height of the generated image.

        Returns
        -------
        PIL.Image:
            The image that was generated.
        """
        image = PIL.Image.new("RGB", (width, height), background)
        draw = PIL.ImageDraw.Draw(image)

        def _draw_character(char: str) -> PIL.Image:
            font = random.choice(self.get_truefonts())
            wid, hei = draw.textsize(char, font=font)

            dx = random.randint(0, 4)
            dy = random.randint(0, 6)
            im = PIL.Image.new("RGBA", (wid + dx, hei + dy))
            PIL.ImageDraw.Draw(im).text((dx, dy), char, font=font, fill=color)

            # rotate
            im = im.crop(im.getbbox())
            im = im.rotate(random.uniform(-30, 30), PIL.Image.BILINEAR, expand=1)

            # warp
            dx = wid * random.uniform(0.1, 0.3)
            dy = hei * random.uniform(0.2, 0.3)
            x1 = int(random.uniform(-dx, dx))
            y1 = int(random.uniform(-dy, dy))
            x2 = int(random.uniform(-dx, dx))
            y2 = int(random.uniform(-dy, dy))
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

        images = []

        for c in chars:
            if random.random() > 0.5:
                images.append(_draw_character(" "))
            images.append(_draw_character(c))

        text_width = sum([im.size[0] for im in images])

        width = max(text_width, width)
        image = image.resize((width, height))

        average = int(text_width / len(chars))
        rand = int(0.25 * average)
        offset = int(average * 0.1)

        for im in images:
            w, h = im.size
            mask = im.convert("L").point(table)
            image.paste(im, (offset, int((height - h) / 2)), mask)
            offset = offset + w + random.randint(-rand, 0)

        if width > width:
            image = image.resize((width, height))

        return image

    def generate(
        self, code_to_generate: str, *, width: Optional[int], height: Optional[int]
    ):
        """Generate the image of the given characters.

        Parameters
        ----------
        code_to_generate: str
            The captcha's code.
        width: Optional[int]
            The width of the captcha image.
        height: Optional[int]
            The height of the captcha image.
        """
        background = random_color(238, 255)
        color = random_color(10, 200, random.randint(220, 255))
        fonts = self.get_truefonts()
        im = self.create_captcha_image(
            code_to_generate,
            color=color,
            background=background,
            width=width,
            height=height,
        )
        self.create_noise_dots(im, color)
        self.create_noise_curve(im, color)
        im = im.filter(PIL.ImageFilter.SMOOTH)
        return im


class TextCaptcha(CaptchaGen):

    # We do that for developer's sanity. When passing fonts is useless here, which would raise
    # an error...
    def __init__(self, **kwargs):
        pass

    def generate(self, code_to_generate: str, **kwargs) -> str:
        return ESCAPE_CHAR.join(code_to_generate)


def random_color(start: int, end: int, opacity: Optional[int] = None) -> tuple:
    r = random.randint(start, end)
    g = random.randint(start, end)
    b = random.randint(start, end)
    if opacity is None:
        return r, g, b
    return r, g, b, opacity
