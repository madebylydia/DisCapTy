#  Copyright (c) 2022​-present - Predeactor - Licensed under the MIT License.
#  See the LICENSE file included with the file for more information about this project's
#   license.

import typing


class Captcha:
    """
    Represent a Captcha object.


    .. py:property:: code
        :type: str

        The code in clear of the Captcha.

    .. py:property:: captcha
        :type: typing.Any

        The captcha object. This is what's send to the user.

    .. py:property:: type
        :type: typing.Any

        The type of the captcha object. It is the same as doing ``type(self.captcha)``.


    .. versionchanged:: 2.0.0
       The Captcha object is no longer what creates the Captcha image, it just is the
       representation of the Captcha that the user will face.
    """

    def __init__(
        self,
        code: str,
        captcha: typing.Any,
    ) -> None:
        self.code = code
        self.captcha = captcha

        self.type = type(self.captcha)

    def __repr__(self) -> typing.Any:
        return self.captcha

    def check(self, text: str, *, force_casing: bool = False, remove_space: bool = True) -> bool:
        # Remove spaces if needed.
        text = text.replace(" ", "") if remove_space else text

        # Lower the text if needed
        text = text.lower() if force_casing else text
        code = self.code.lower() if force_casing else self.code

        # Result of the check.
        return code == text
