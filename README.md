# DisCapTy

![DisCapTy's Logo](.github/logo.png#gh-dark-mode-only)![DisCapTy's Logo](.github/logo-dark.png#gh-light-mode-only)

DisCapTy is a highly type hinted Python module to generate Captcha images without struggling your mind on how to make your own. Everyone can use it!

**Documentation:** <https://discapty.readthedocs.io/>

<div align="center">
    <a href="https://pypi.org/project/DisCapTy/">
        <img src="https://img.shields.io/pypi/v/discapty?style=flat-square" alt="DisCapTy's Version" />
        <img src="https://img.shields.io/pypi/pyversions/discapty?style=flat-square" alt="Python Version Required" />
        <img src="https://img.shields.io/pypi/dm/discapty?color=blue&style=flat-square" alt="DisCapTy's download" />
    </a>
    <a href="https://discapty.readthedocs.io/en/latest/?badge=latest">
        <img src="https://readthedocs.org/projects/discapty/badge/?version=latest&style=flat-square" alt="Documentation Status" />
    </a>
</div>

## Installing

DisCapTy is available on PyPi!

```sh
pip3 install discapty
```

To use DisCapTy, you need a Python version equal or greater to `3.7` and below `3.11`.

## Clone & Test the project

This project is dependant of [Poetry](https://python-poetry.org), a dependency management tool. You are most likely going to require this tool to correctly interact with the project & its dependencies, check out [Poetry's documentation](https://python-poetry.org/docs) for how to install it.

To clone the repository: `git clone https://github.com/Predeactor/DisCapTy.git`

To install dependencies: `poetry install`

To run tests: `poetry run python -m unittest`

## Creating Captcha

For DisCapTy, a Captcha is simply a code with any possible objects that can be returned, for example, it is one code (Like "12345") with an image (Usually a `PIL.Image.Image` object)
This is because DisCapTy uses the concept of generators that are used to generate a captcha from a given code, and it can return anything.

DisCapTy comes with 3 builtin generators:

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

if captcha.check(user_input) is True:
    # The user input is correct
    print("Correct!")
else:
    # The user input is incorrect
    print("Incorrect!")
```

What's great with the `.check` method is that you can specify if you need to remove space in the user's input and/or check casing.

Creating Captcha manually is not a recommended way, because DisCapTy comes with its opinionated challenge runner & is inefficient anyway.

### Create a Challenge

```py
import discapty

challenge = discapty.Challenge(discapty.TextGenerator(), retries=3)

captcha = challenge.begin()

# We cannot provide typehint here, `captcha` is a `typing.Any` and cannot help you, it'll be your
# job to know what you'll get as a captcha.
send_captcha_to_user(captcha)
user_input: str = get_user_input()

is_correct: bool = challenge.check(user_input)
# If the user's input is correct, the challenge ends, if not, `challenge.attempted_tries` will get
# +1, and if it is greater than the retries that has been set, then an error is raised when using
# `.check`
```

Please see the [documentation](https://discapty.readthedocs.io/) for more information on how the library work.

## Contact

You can join my Discord server for any help: <https://discord.gg/aPVupKAxxP>

DisCapTy is an open-source project distributed under the MIT license:
![PyPI - License](https://img.shields.io/pypi/l/discapty?style=flat-square)

DisCapTy uses the [Roboto](https://fonts.google.com/specimen/Roboto) font as default font.
[This font](https://fonts.google.com/specimen/Roboto) is licensed under [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).
