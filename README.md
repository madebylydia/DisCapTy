# DisCapTy [![Verified on Openbase](https://badges.openbase.com/python/verified/DisCapTy.svg?style=openbase)](https://openbase.com/python/DisCapTy?utm_source=embedded&amp;utm_medium=badge&amp;utm_campaign=rate-badge)

![DisCapTy's Logo](.github/discapty.png)

DisCaPty is a Python module to generate Captcha images without struggling your mind on how to make your own. Everyone can use it!

**Documentation:** https://discapty.readthedocs.io/

![PyPI](https://img.shields.io/pypi/v/discapty)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/discapty)
![PyPI - Downloads](https://img.shields.io/pypi/dm/discapty?color=blue)
[![Documentation Status](https://readthedocs.org/projects/discapty/badge/?version=latest)](https://discapty.readthedocs.io/en/latest/?badge=latest)


## Installing

DisCaPty is available on PyPi!

```sh
pip3 install discapty
```

To use DisCapTy, you need a Python version equal or greater to `3.10`.

## Clone & Test the project

This project is dependant of [Poetry](https://python-poetry.org), a dependency management tool. You are most likely going to require this tool to correctly interact with the project & its dependencies, check out [Poetry's documentation](https://python-poetry.org/docs) for how to install it.

After then, clone the repository & run `poetry install`

## Creating Captcha

For DisCapTy, a Captcha is simply a code with any possible objects that can be returned, for example, it is one code (Like "12345") with an image (Usually a `PIL.Image.Image` object)
This is because DisCapTy uses the concept of generators that are used to generate a captcha from a given code, and it can return anything.

DisCapTy comes with 2 builtin generators:
- TextGenerator : Text based captcha
- WheezyGenerator : Image based captcha
- ImageGenerator : Image based captcha

### Creating Captcha manually

```py
import discapty

def generate_a_captcha(initial_input: str) -> discapty.Captcha:
    # This generator returns an obfuscated text.
    captcha_for_user = discapty.TextGenerator().generate(initial_input)
    # Create a Captcha object, the first argument is the clear code, the second is the obfuscated code. Anything goes.
    return discapty.Captcha(initial_input, captcha_for_user)

# Generate your Captcha.
captcha = generate_a_captcha("12345")

# Show the obfuscated code. See https://discapty.readthedocs.io for more information on this object.
show_captcha_to_user(captcha.captcha)
```

### Checking user's input

```py
import discapty

# Generate your Captcha.
captcha: discapty.Captcha = generate_a_captcha("12345")

# This is your user's input here
user_input: str = '12345'

if captcha.check(user_input):
    # The user input is correct
    print("Correct!")
else:
    # The user input is incorrect
    print("Incorrect!")
```

What's great with the `.check` method is that you can specify if you need to remove space in the user's input and/or check casing.

This is not a recommended way, because DisCapTy comes with its opinionated challenge runner.



## Contact

You can join my Discord server for any help: https://discord.gg/aPVupKAxxP

DisCapTy is an open-source project distributed under the MIT license:
![PyPI - License](https://img.shields.io/pypi/l/discapty?style=flat-square)

DisCapTy uses the [Roboto](https://fonts.google.com/specimen/Roboto) font as default font.
[This font](https://fonts.google.com/specimen/Roboto) is licensed under [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).
