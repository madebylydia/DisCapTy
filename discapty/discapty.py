from datetime import datetime
from os import PathLike
from io import BytesIO
from typing import Optional, Union, List, Tuple

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

        Raises
        ------
        KeyError:
            The given captcha type is not available in DisCapTy.
        """
        if captcha_type not in TYPES:
            raise KeyError("Given type %s is not available." % captcha_type)
        self.code: str = code or random_code()

        # Get classe and initialize
        self.captcha: Union[WheezyCaptcha, ImageCaptcha, TextCaptcha] = TYPES[
            captcha_type
        ](fonts=fonts, fonts_sizes=fonts_sizes)

    def setup(self):
        pass

    def generate_captcha(self) -> Union[BytesIO, str]:
        """Generate the captcha image or text.
        In case the choosen captcha type is TextCaptcha, a string will be returned, otherwise
        it will be a BytesIO object.

        Returns
        -------
        io.BytesIO: The image. Can be used as a file to send. If the captcha type is text, a
            string will be returned instead.
        """

        if not isinstance(self.captcha, TextCaptcha):
            image: Image = self.captcha.generate(self.code)
            out = BytesIO()
            # Typehint think it's Union[BytesIO, str] which trigger PyLint
            # noinspection PyUnresolvedReferences
            image.save(out, format="png")
            out.seek(0)
            return out

        return self.captcha.generate(random_code())

    def generate_embed(
        self,
        guild_name: str,
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
            - Setting the embed's title: ``title`` (Make guild_name parameter unuseful)
            - Setting the embed's description: ``description``
            - Setting the embed's timestamp: ``timestamp``
            - Setting the embed's thumbnail: ``thumbnail``
            - Setting the embed's image URL: ``image_url``. By default
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
        title = kwargs.get("title", f"{guild_name} Captcha Verification")
        _type = kwargs.get("type", "rich")
        title_url = kwargs.get("title_url", discord.embeds.EmptyEmbed)
        timestamp = kwargs.get("timestamp", discord.embeds.EmptyEmbed)
        thumbnail = kwargs.get("thumbnail", discord.embeds.EmptyEmbed)
        description = kwargs.get(
            "description", "Please return the code written on the captcha."
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
        CopyPasteError:
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
