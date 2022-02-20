from typing import TypedDict, Union

class ChallengeOptions(TypedDict):
    retries: int


class Challenge:
    """
    Representation of a challenge. A challenge is a class who's job is to 
    """

    def __init__(self, **kwargs: Union[str, int]) -> None:
        self.is_active: bool = False
        self.code: str = "None"

        self.retries: int = kwargs.get('retries') or 3

    def begin(self):
        self.is_active = True

    def verify(self, code: str):
        pass
