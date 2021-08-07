from datetime import datetime
from os import PathLike
from io import BytesIO
from typing import Optional, Union, List, Tuple, NoReturn
from string import Template

# noinspection PyPackageRequirements
import discord
from PIL import Image

from .exceptions import CopyPasteError
from .generator import ImageCaptcha, TextCaptcha, WheezyCaptcha
from .typehint import Author, Footer
from .utils import ESCAPE_CHAR, random_code

TYPES = {
    "wheezy": WheezyCaptcha,
    "image": ImageCaptcha,
    "text": TextCaptcha,
}


class Captcha:
    """The representation of a captcha.

    This is the class that will create the captcha and his code if necessary.
    """

    def __init__(
        self,
        captcha_type: TYPES,
        *,
        code: Optional[str] = None,
        fonts: Optional[List[Union[PathLike, str]]] = None,
        fonts_sizes: Optional[Tuple[int]] = None,
    ):
        """
        Initializes class instance.

        Parameters
        ----------
        captcha_type: str
            What kind of captcha must be generated.
            Can be either "image", "wheezy" or "text".
        code: str
            The code you wish to use with the captcha. Optional. If none is given,
            a random code is generated.
        fonts: Optional[List[Union[PathLike, str]]]
            A list of path to custom fonts.
        fonts_sizes: Optional[Tuple[int]]
            A tuple of font's size. When generating a letter/number on the image, a random
            number will be taken in this tuple.

        Raises
        ------
        KeyError:
            The given captcha type is not available in DisCapTy.
        OSError:
            The fonts cannot be opened. most probably due to an incorrect path.
        """
        if captcha_type not in TYPES:
            raise KeyError("Given type %s is not available." % captcha_type)
        self.code: str = code or random_code()

        # Get classe and initialize
        self.captcha: Union[WheezyCaptcha, ImageCaptcha, TextCaptcha] = TYPES[
            captcha_type
        ](fonts=fonts, fonts_sizes=fonts_sizes)

        self._settings: dict = {
            # General
            "width": 300,
            "height": 125,
            "background_color": "#EEEECC",
            "text_color": "#5C87B2",
            # image specific
            "number_of_dots": 30,
            "width_of_dots": 3,
            "number_of_curves": 1,
            # wheezy specific
            "text_squeeze_factor": 0.8,
            "noise_number": 30,
            "noise_color": "#EEEECC",
            "noise_level": 2,
        }

    def setup(self, **kwargs) -> NoReturn:
        """
        Set differents parameters for the captcha to generate.

        Parameters width, height, background_color and text_color are applied to any types.
        Parameters number_of_dots, width_of_dots and number_of_curves are specific to image type.
        Parameters text_squeeze_factor, noise_number, noise_color, noise_level are specific to
        wheezy type.
        Any of this parameters will be applied to the text type.
        Unknown parameters will be ignored.

        Parameters
        ----------
        width: int
            The width of the image.
        height:
            The height of the image.
        background_color: str
            A string of the HEX code to use for the background and effects.
            Support transparency.
        text_color: str
            A string of the HEX code to use for the text.
            Support transparency.

        number_of_dots: int
            The number of dots to generate on the image if applicable.
            Specific to image type. Defaults to 30.
        width_of_dots: int
            The width of dots to generate on the image if applicable.
            Specific to image type. Defaults to 3px.
        number_of_curves: int
            The number of curves to generate on the image if applicable.
            Specific to image type. Defaults to 1.

        text_squeeze_factor: float
            How much space there is between characters. Specific to wheezy type.
            Defaults to 0.8.
        noise_number: int
            How much noise will be generated on the image. Specific to wheezy type.
            Defaults to 30.
        noise_color: str
            The noise's color. Specific to wheezy type.
            Defaults to #EEEECC. Support transparency.
        noise_level: int
            How hard the noise will be. Specific to wheezy tupe.
            Defaults to 2.
        """
        can_be_setup = [setting for setting in self._settings]
        settings = [arg for arg in kwargs.items() if arg[0] in can_be_setup]
        for setting in settings:
            self._settings[setting[0]] = setting[1]

    def generate_captcha(self) -> Union[BytesIO, str]:
        """Generate the captcha image or text.
        In case the choosen captcha type is text, a string will be returned, otherwise
        it will be a BytesIO object.

        Returns
        -------
        Union[io.BytesIO, str]
            The captcha object. It is a string if the type is text, otherwise it is a png
            image put into a BytesIO object.
        """

        if not isinstance(self.captcha, TextCaptcha):
            image: Image = self.captcha.generate(self.code, **self._settings)
            out = BytesIO()
            # Typehint think it's Union[BytesIO, str] which trigger PyLint
            # noinspection PyUnresolvedReferences
            image.save(out, format="png")
            out.seek(0)
            return out

        return self.captcha.generate(self.code)

    def generate_embed(
        self,
        guild_name: Optional[str] = None,
        *,
        author: Optional[Author] = None,
        footer: Optional[Footer] = None,
        **kwargs,
    ) -> discord.Embed:
        """
        Generate a pre-build embed for your guild. Can be customized with kwargs.

        If you're generating a captcha that is not a TextCaptcha, an image can be uploaded
        inside the captcha by sending an attachment with the captcha that is called
        "captcha.png". Can be modified with ``image_url`` in kwargs.
        The code is automatically added to the description when using TextCaptcha.

        Parameters
        ----------
        guild_name: str
            The name of the guild we are generating the embed for. Will be shown on
            the embed title if not edited.
        author: Optional[Dict[str, str]]
            A mapping that can contain ``name`` and ``url`` as the key, they will be
            shown at the author field. (Top of the embed). Optional.
            ``name`` will be the text and ``url`` the icon's URL that will be shown.
        footer: Optional[Dict[str, str]]
            A mapping that can contain ``text`` and ``url`` as the key, they will be
            shown on the footer. (Bottom of the embed). Optional.
            ``text`` will be the text and ``url`` the icon's URL that will be shown.
        **kwargs:
            Set given parameters as the content of the embed.
            The kwarg name can be either:
            - Setting the embed's color: ``colour`` or ``color``
            - Setting the embed's clickable URL on title: ``title_url``
            - Setting the embed's title: ``title`` (Overwrite guild_name parameter)
            - Setting the embed's description: ``description``
            In case your captcha's type use text, you can put "$code" in your string and
            it will automatically replaced by the captcha's code.
            Example:
            ```Please send me `$code`.```
            will return the following description in the embed:
            ```Please send me `FKLAC63`.```

            - Setting the embed's timestamp: ``timestamp``
            - Setting the embed's thumbnail: ``thumbnail``
            - Setting the embed image's URL: ``image_url``. By default
            ``attachment://captcha.png``.

        Return
        ------
        discord.Embed: The generated embed.
        """

        # Part of the code taken from Cog-Creators/Red-DiscordBot.
        # https://github.com/Cog-Creators/Red-DiscordBot/blob/b2db0674d5b4256c4747e1ac17e08f156241a206/redbot/cogs/audio/core/utilities/miscellaneous.py#L66
        # Basically, this part allow developers to use parameters to set different fields in the embed.

        # Get everything we need from kwargs.
        colour = kwargs.get("colour") or kwargs.get("color")
        title = kwargs.get(
            "title",
            f"{guild_name} Captcha Verification"
            if guild_name
            else "Captcha Verification",
        )
        _type = kwargs.get("type", "rich")
        title_url = kwargs.get("title_url", discord.embeds.EmptyEmbed)
        timestamp = kwargs.get("timestamp", discord.embeds.EmptyEmbed)
        thumbnail = kwargs.get("thumbnail", discord.embeds.EmptyEmbed)
        if isinstance(self.captcha, TextCaptcha):
            description = Template(
                kwargs.get(
                    "description",
                    "Please return the code written on the Captcha: $code",
                )
            ).safe_substitute({"code": self.generate_captcha()})
        else:
            description = kwargs.get(
                "description", "Please return me the code written on the Captcha."
            )
        contents = dict(title=title, type=_type, url=title_url, description=description)

        # Obtaining or creating embed.
        if hasattr(kwargs.get("embed"), "to_dict"):
            embed = kwargs.get("embed")
            if embed is not None:
                embed = embed.to_dict()
        else:
            embed = {}

        # Setting up the rest...
        colour = embed.get("color", None) or colour or discord.embeds.Colour.default()
        contents.update(embed)
        if timestamp and isinstance(timestamp, datetime):
            contents["timestamp"] = timestamp
        embed = discord.Embed.from_dict(contents)
        embed.color = colour
        if footer:
            text = footer.get("text", discord.embeds.EmptyEmbed)
            url = footer.get("url", discord.embeds.EmptyEmbed)
            embed.set_footer(text=text, icon_url=url)
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        if author:
            name = author.get("name", discord.embeds.EmptyEmbed)
            url = author.get("url", discord.embeds.EmptyEmbed)
            embed.set_author(name=name, icon_url=url)

        if not isinstance(self.captcha, TextCaptcha):
            embed.set_image(url=kwargs.get("image_url", "attachment://captcha.png"))

        return embed

    def verify_code(self, user_input: str, *, ignore_case: bool = False):
        """Verify the code with the generated code.

        Parameters
        ----------
        user_input: str
            The code we are verifying.
        ignore_case: bool
            Verificating ignore case by default, overwrite this parameter to make the
            verification important to lower and upper case.

        Raises
        ------
        discapty.CopyPasteError:
            If the code is the same as what was generated when generating the captcha code of
            PlainCaptcha.

        Return
        ------
        bool:
            If the code is equal the same that what was generated.
        """
        obfuscated_code = ESCAPE_CHAR.join(self.code)
        if not ignore_case:
            user_input = user_input.lower()
            code = self.code.lower()
            obfuscated_code = obfuscated_code.lower()
        else:
            code = self.code

        if isinstance(self.captcha, TextCaptcha) and user_input == obfuscated_code:
            raise CopyPasteError()
        return user_input == code
