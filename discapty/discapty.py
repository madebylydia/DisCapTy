# noinspection PyPackageRequirements
import discord
from io import BytesIO
from string import ascii_uppercase, digits
from random import SystemRandom
from typing import Union
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
        self,
        guild_name: str,
        *,
        title: str = None,
        description: str = None,
        embed_color: int = None,
        **kwargs
    ) -> dict:
        """
        Generate a pre-build embed for your guild.

        :param guild_name: The name of the guild we are generating the embed for.
        :param title: The title of the embed. Defaults to "{GuildName} Captcha Verification".
        :param description: The description of the embed. If ommited, a text is generated,
            depending on the type of the captcha, the text will be slightly different.
        :param embed_color: The color of the embed you specifically want. If ommited, a random
            color is generated.

        :return: A dict containing the embed and the image to send if necessary, can be None.
            >>> {"embed": discord.Embed, "image": discord.File or None}
            This is what must be used for sending the captcha.
        """
        if embed_color is None:
            embed_color = discord.Colour.random().value
        title = title or "{guild} Captcha Verification".format(guild=guild_name)
        captcha = await self.generate_captcha()
        if isinstance(self.captcha, PlainCaptcha):
            description = "Please return me the following code:\n```{code}```\nDo not copy and paste.".format(
                code=captcha
            )
        else:
            description = (
                description or "Please return me the code written on the following image."
            )
        embed = discord.Embed(title=title, description=description, colour=embed_color, **kwargs)
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

        :raise: SameCodeError: If the code is the same as what was generated when generating the
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
        if user_input.replace("\u200B", "") != code:
            return False
        return True
