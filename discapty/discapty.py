from datetime import datetime
# noinspection PyPackageRequirements
import discord
from io import BytesIO
from string import ascii_uppercase, digits
from random import SystemRandom
from typing import Union, Mapping
from .generator import WheezyCaptcha, ImageCaptcha, PlainCaptcha


def random_code(length: int = 8):
    return "".join(SystemRandom().choice(ascii_uppercase + digits) for _ in range(length))


types = {
    "wheezy": WheezyCaptcha(width=350, height=100),
    "image": ImageCaptcha(width=350, height=100),
    "plain": PlainCaptcha(),
}


class SameCodeError(Exception):
    """
    An error raised if the user sent the exact same code of the generated code when using a
    PlainCaptcha captcha type.
    """

    pass


class Captcha:
    """The representation of a captcha.

    This is the class that will create the captcha and his code if necessary.

    """

    def __init__(self, captcha_type: types, *, code: str = None):
        """
        Initializes class instance.

        :param captcha_type: What kind of captcha must be generated.
            Can be either "image", "plain" or "wheezy".
        :param code: The code you wish to use with the captcha.
        """
        if captcha_type not in types:
            raise KeyError("Given type {type} is not available.".format(type=captcha_type))
        self.code: str = code or random_code()
        self.generated_code: str = code  # This is in case we are using PlainCaptcha.
        self.captcha: types = types[captcha_type]

    async def generate_captcha(
        self, code: str = None, *, force_no_edit: bool = False
    ) -> Union[BytesIO, str]:
        """Generate the captcha image.
        In case the choosen captcha type is plain, a string will be returned.

        :param code: Optional. The code that must be used. If omitted, the class that was set
            on class inheritance will be used. Using this parameter will overwrite the old
            self.code with the one given.
        :param force_no_edit: Optional. If you do not want to overwrite the code when using "code"
            parameter. Defaults to False.

        :return: A BytesIO objecting containing the image, can be used as a file to send. If the
            captcha type is an instance of PlainCaptcha, a string will be returned.
        """
        if code and not force_no_edit:
            self.code = code
        if not isinstance(self.captcha, PlainCaptcha):
            image = await self.captcha.generate(self.code)
            out = BytesIO()
            image.save(out, format="png")
            out.seek(0)
            return out
        self.generated_code = await self.captcha.generate(self.code)
        return self.generated_code

    async def generate_embed(
        self, guild_name: str,
        author: Mapping[str, str] = None,
        footer: Mapping[str, str] = None,
        **kwargs
    ) -> dict:
        """
        Generate a pre-build embed for your guild.

        :param guild_name: The name of the guild we are generating the embed for. Will be shown on
            the embed title if not edited.
        :param author: A mapping that can contain ``name`` and ``url`` as the key, they will be
            shown at the author field. (Top of the embed)
            ``name`` will be the text and ``url`` the icon's URL that will be shown.
        :param footer: A mapping that can contain ``text`` and ``url`` as the key, they will be
            shown on the footer. (Bottom of the embed)
            ``text`` will be the text and ``url`` the icon's URL that will be shown.

        :param kwargs: Set given parameters as the content of the embed.
            The kwarg name can be either:
            - Setting the embed's color: ``colour`` or ``color``
            - Setting the embed's clickable URL on title: ``title_url``
            - Setting the embed's title: ``title`` (Make guild_name parameter unuseful)
            - Setting the embed's description: ``description``
            - Setting the embed's timestamp: ``timestamp``
            - Setting the embed's thumbnail: ``thumbnail``

        :return: A dict containing the embed and the image to send if necessary, can be None.
            >>> {"embed": discord.Embed, "image": discord.File or None}
            This is what must be used for sending the captcha.
        """

        # Part of the code "stolen" to Cog-Creators/Red-DiscordBot.
        # https://predeactor.please-end.me/AILdT65
        # Basically, this part allow creators to use parameters to set different fields in the embed.

        # Get everything we need from kwargs.
        colour = kwargs.get("colour") or kwargs.get("color")
        title = kwargs.get("title", "{guild} Captcha Verification".format(guild=guild_name))
        _type = kwargs.get("type", "rich") or "rich"
        title_url = kwargs.get("title_url", discord.embeds.EmptyEmbed) or discord.embeds.EmptyEmbed
        timestamp = kwargs.get("timestamp", discord.embeds.EmptyEmbed) or discord.embeds.EmptyEmbed
        thumbnail = kwargs.get("thumbnail", discord.embeds.EmptyEmbed) or discord.embeds.EmptyEmbed
        description = (
            kwargs.get("description", "Please return me the code written on the following image.")
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

        captcha = await self.generate_captcha()
        if isinstance(self.captcha, PlainCaptcha):
            embed.description = "Please return me the following code:\n```{code}```\nDo not copy and paste.".format(
                code=captcha
            )
        if not isinstance(self.captcha, PlainCaptcha):
            embed.set_image(url="attachment://captcha.png")

        return {
            "embed": embed,
            "image": discord.File(captcha, filename="captcha.png")
            if not isinstance(self.captcha, PlainCaptcha)
            else None,
        }

    async def verify_code(self, user_input: str, *, ignore_case: bool = True):
        """Verify the code with the generated code.

        :param user_input: The code we are verifying.
        :param ignore_case: Verificating ignore case by default, overwrite this
            parameter to make the verification important to lower and upper case.

        :raise SameCodeError: If the code is the same as what was generated when generating the
            captcha code of PlainCaptcha.

        :return: A boolean representing if the code is equal to what was generated.
        """
        obfuscated_code = self.generated_code
        code = self.code
        if ignore_case:
            user_input = user_input.upper()
            code = self.code.upper()
            if obfuscated_code is not None:
                obfuscated_code = obfuscated_code.upper()
        if isinstance(self.captcha, PlainCaptcha):
            if user_input == obfuscated_code:
                raise SameCodeError()
        if user_input != code:
            return False
        return True
