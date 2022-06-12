import typing
from random import randint, random, uniform
from secrets import choice

from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont

from discapty.wheezylib.bezier import make_bezier


def captcha(
    drawings: typing.Sequence[typing.Callable[[Image.Image, str], Image.Image]],
    width: int = 200,
    height: int = 75,
) -> typing.Callable[[str], Image.Image]:
    def render(text_input: str) -> Image.Image:
        img = Image.new("RGB", (width, height), (255, 255, 255))
        for drawing in drawings:
            img = drawing(img, text_input)
        return img

    return render


# Drawings


def background(background_color: str = "#EEEECC"):
    color = ImageColor.getrgb(background_color)

    def render(image: Image.Image, _: str) -> Image.Image:
        ImageDraw.Draw(image).rectangle(((0, 0), image.size), fill=color)
        return image

    return render


def apply_filter(img_filter: ImageFilter.Filter):
    """
    Filter an image with the given filter.
    """

    def render(image: Image.Image, _: str) -> Image.Image:
        return image.filter(img_filter)

    return render


def apply_filters(filters: typing.Sequence[ImageFilter.Filter]):
    """
    Filter an image with the given filters.
    """

    def render(image: Image.Image, _: str) -> Image.Image:
        for image_filter in filters:
            image = image.filter(image_filter)
        return image

    return render


def smooth():
    def render(image: Image.Image, _: str) -> Image.Image:
        return image.filter(ImageFilter.SMOOTH)

    return render


def curve(
    curve_color: str = "#5C87B2", *, curve_width: int = 4, curve_number: int = 6
) -> typing.Callable[[Image.Image, str], Image.Image]:
    color = ImageColor.getrgb(curve_color)

    def render(image: Image.Image, _: str):
        width, height = image.size
        dx = width / curve_number
        path = [(dx * i, randint(0, height)) for i in range(1, curve_number)]
        all_coefs = make_bezier(curve_number - 1)
        points = [
            tuple(sum(coef * p for coef, p in zip(coefs, ps)) for ps in zip(*path))
            for coefs in all_coefs
        ]

        ImageDraw.Draw(image).line(points, fill=color, width=curve_width)  # type: ignore
        return image

    return render


def noise(
    noise_color: str = "#EEEECC",
    *,
    noise_number: int = 50,
    noise_width: int = 2,
) -> typing.Callable[[Image.Image, str], Image.Image]:
    color = ImageColor.getrgb(noise_color)

    def render(image: Image.Image, _: str):
        width, height = image.size
        dx = width / 10
        width = width - dx
        dy = height / 10
        height = height - dy
        draw = ImageDraw.Draw(image)

        for __ in range(noise_number):
            x = int(uniform(dx, width))
            y = int(uniform(dy, height))
            draw.line(((x, y), (x + noise_width, y)), fill=color, width=noise_width)

        return image

    return render


def text(
    fonts: typing.Sequence[str],
    fonts_sizes: typing.Tuple[int, ...],
    *,
    drawings: typing.Optional[typing.Sequence[typing.Callable[[Image.Image], Image.Image]]],
    text_color: str = "#5C87B2",
    squeeze_factor: float = 0.8,
) -> typing.Callable[[Image.Image, str], Image.Image]:
    tt_fonts = tuple([ImageFont.truetype(name, size) for name in fonts for size in fonts_sizes])
    color = ImageColor.getrgb(text_color)

    def render(image: Image.Image, text_input: str) -> Image.Image:
        draw = ImageDraw.Draw(image)

        # We will make a loop for each character in input, so we can
        # use drawings on each character and create a more wheezy-like
        # result.
        # In the end, we will paste those characters in the image.
        characters: typing.List[Image.Image] = []

        for input_character in text_input:
            # Mostly setting up things here...
            rand_font = choice(tt_fonts)
            char_width, char_height = draw.textsize(input_character, font=rand_font)
            character = Image.new("RGB", (char_width, char_height), (0, 0, 0))
            character_draw = ImageDraw.Draw(character)

            # Draw the actual character
            character_draw.text((0, 0), input_character, fill=color, font=rand_font)  # type: ignore
            character = character.crop(character.getbbox())

            # Applies drawings
            if drawings:
                for drawing in drawings:
                    character = drawing(character)

            characters.append(character)

        width, height = image.size
        image_offset = int(
            (
                width
                - sum(int(i.size[0] * squeeze_factor) for i in characters[:-1])
                - characters[-1].size[0]
            )
            / 2
        )

        # Paste characters into final image
        for character in characters:
            character_width, character_height = character.size
            mask = character.convert("L").point(lambda x: int(x * 1.97))  # type: ignore
            image.paste(character, (image_offset, int((height - character_height) / 2)), mask)
            image_offset += int(character_width * squeeze_factor)

        return image

    return render


def warp(
    dx_factor: float = 0.27, dy_factor: float = 0.21
) -> typing.Callable[[Image.Image], Image.Image]:
    def render(image: Image.Image) -> Image.Image:
        width, height = image.size
        dx = width * dx_factor
        dy = height * dy_factor
        x1 = int(uniform(-dx, dx))
        y1 = int(uniform(-dy, dy))
        x2 = int(uniform(-dx, dx))
        y2 = int(uniform(-dy, dy))

        new_image = Image.new("RGB", (width + abs(x1) + abs(x2), height + abs(y1) + abs(y2)))
        new_image.paste(image, (abs(x1), abs(y1)))
        width, height = new_image.size
        return new_image.transform(
            (width, height),
            Image.QUAD,
            (
                x1,
                y1,
                -x1,
                width - y2,
                height + x2,
                width + y2,
                height - x2,
                -y1,
            ),
        )

    return render


def offset(
    dx_factor: float = 0.1, dy_factor: float = 0.2
) -> typing.Callable[[Image.Image], Image.Image]:
    def render(image: Image.Image) -> Image.Image:
        width, height = image.size
        dx = int(random() * width * dx_factor)
        dy = int(random() * height * dy_factor)
        new_image = Image.new("RGB", (width + dx, height + dy))
        new_image.paste(image, (dx, dy))
        return new_image

    return render


def rotate(angle: int = 25) -> typing.Callable[[Image.Image], Image.Image]:
    def render(image: Image.Image):
        return image.rotate(uniform(-angle, angle), Image.BILINEAR, expand=True)

    return render
