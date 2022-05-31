from typing import Any


class Captcha:
    """
    Represent a Captcha image.
    """

    def __init__(self, code: Any, generator: str) -> None:
        self.code = code
        self._generated_by = generator
