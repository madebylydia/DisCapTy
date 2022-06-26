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
        captcha_object: typing.Any,
    ) -> None:
        self.code = code
        self.captcha_object = captcha_object

        self.type = type(self.captcha_object)

    def __repr__(self) -> typing.Any:
        return f"<Captcha type={self.type}>"

    def check(self, text: str, *, force_casing: bool = False, remove_spaces: bool = True) -> bool:
        """
        Check if a text is correct to the captcha code.

        Parameters
        ----------
        text : str
            The answer to check against the Captcha's code.
        force_casing : bool
            If True, the casing must be respected. Defaults to False.
        remove_spaces : bool
            If True, spaces will be removed when checking the answer. Defaults to True.

        Return
        ------
        bool:
            True if the answer is correct, False otherwise.

        """
        # Remove spaces if needed.
        text = text.replace(" ", "") if remove_spaces else text

        # Lower the text if needed
        text = text if force_casing else text.lower()
        code = self.code if force_casing else self.code.lower()

        # Result of the check.
        return code == text
