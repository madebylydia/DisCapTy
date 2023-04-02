import typing

_CR = typing.TypeVar("_CR")


class Captcha(typing.Generic[_CR]):
    """
    Represent a Captcha object.


    .. versionchanged:: 2.0.0
       The Captcha object is no longer what creates the Captcha image, it just is the
       representation of the Captcha that the user will face.

    .. versionchanged:: 2.1.0
       This class is now a generic class and requires to indicate which type it will receive.
       (If necessary)
    """

    code: str
    captcha_object: _CR
    type: typing.Type[_CR]

    def __init__(
        self,
        code: str,
        captcha_object: _CR,
    ) -> None:
        self.code = code
        self.captcha_object = captcha_object
        self.type = type(self.captcha_object)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Captcha type={self.type}>"

    def check(self, text: str, *, force_casing: bool = False, remove_spaces: bool = True) -> bool:
        """
        Check if a text is correct against the captcha code.

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
