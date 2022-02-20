class UnexistingChallengeError(KeyError):
    """
    Raised when trying to get a challenge that does not exist.
    Subclass of "KeyError" as this error will appear when trying to get the challenge from a dict.
    """

class InvalidFont(Exception):
    """
    Raised when one or more fonts are invalid.
    """
