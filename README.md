# DisCapTy [![Verified on Openbase](https://badges.openbase.com/python/verified/DisCapTy.svg?style=openbase)](https://openbase.com/python/DisCapTy?utm_source=embedded&amp;utm_medium=badge&amp;utm_campaign=rate-badge)

![DisCapTy's Logo](.github/discapty.png)

DisCaPty is a Python module to generate Captcha images without struggling your mind on how to make your own. Everyone can use it!

**Documentation:** https://discapty.readthedocs.io

![PyPI](https://img.shields.io/pypi/v/discapty)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/discapty)
![PyPI - Downloads](https://img.shields.io/pypi/dm/discapty?color=blue)
[![Documentation Status](https://readthedocs.org/projects/discapty/badge/?version=latest)](https://discapty.readthedocs.io/en/latest/?badge=latest)


# Installing

DisCaPty is available on PyPi!

```sh
pip3 install discapty
```
You require a version higher

# Clone & Test the project

This project is dependant of [Poetry](), a dependency managemer tool. You are most likely going to require this tool to correctly interact with the project, check out [Poetry's documentation](https://python-poetry.org/docs) for how to install it.

After then, clone the repository & run `poetry install`

# Creating Captcha

DisCapTy include 3 differents types of Captcha style.
- text: A Captcha that use plain text. This type is particular as it include a zero width space character between each letter/number to unallow the user to copy/paste the captcha.
- wheezy: An image Captcha, pretty basic and easy to read. Configurable
- image: An image Captcha, a bit more hard to read, less user friendly. Configurable.

You can choose which type to use when creating a Captcha object.

Example:

```py
import discapty

captcha = discapty.Captcha("wheezy")
# You are initializing a Captcha object that is the "wheezy" type.
# If you want to show the image/captcha, use generate_captcha()
captcha_image = captcha.generate_captcha()  # <_io.BytesIO object at XxXXX>
```

However, using the "text" type will not return a BytesIO object but a string.

```py
import discapty

captcha = discapty.Captcha("text_color")
captcha_image = captcha.generate_captcha()  # This will return a string, not a BytesIO object.
```

You can also easily create an embed.

```py
import discapty


async def send_captcha(ctx):
    captcha = discapty.Captcha("image")
    captcha_image = discord.File(captcha.generate_captcha(),
                                 filename="captcha.png")  # This is # # important to put this filename, otherwise Discord will send the image outside of the embed.
    # You can change it when generating the embed.
    captcha_embed = captcha.generate_embed(ctx.guild.name)
    await ctx.channel.send(embed=captcha_embed, file=captcha_image)
```

# Create more complex Captcha

The power of DisCapTy is how it let you customize your Captcha by using the setup function.
**When using this function, it is recommended to use number that are reasonable enough to not overload your machine. Image creation may take time if you abuse of it, and memory can also go high.**

```py
import discapty


def generate_captcha():
    captcha = discapty.Captcha("wheezy")

    # This function is what allow developers to set addition settings for their captcha, refer to the function's help for more parameters to use.
    captcha.setup(width=400, height=400, noise_color="#FF0000")

    return discapty.generate_embed()  # Return the image with the settings that has been set.
```

# Contact

You can join my Discord server for any help: https://discord.gg/aPVupKAxxP

DisCapTy is licensied under MIT: ![PyPI - License](https://img.shields.io/pypi/l/discapty)

DisCapTy use the Roboto font as default font.
This font is licensied under [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).
