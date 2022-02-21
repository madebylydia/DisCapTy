from typing import TypedDict, Union

class ChallengeOptions(TypedDict):
    retries: int


class Challenge:
    """
    Representation of a challenge. A challenge represent the user's Captcha challenge he must
    face.
    
    This class takes cares of:
        - Generating the captcha
        - Verify inputs
        - Manage the "Captcha" object
    
    It free your mind from managing all the process of a captcha challenge, keeping your code
    short and easy.
    """

    def __init__(self, **kwargs: Union[str, int]) -> None:
        self.is_active: bool = False
        self.code: str = "None"

        self.retries: int = kwargs.get('retries') or 3

    def begin(self):
        self.is_active = True

    def verify(self, code: str):
        pass
