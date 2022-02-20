from typing import Any, Dict
# from pathlib import Path

# from PIL import ImageFont

from discapty.challenge import Challenge

from .errors import UnexistingChallengeError

class CaptchaQueue:
    """
    A safe handler for all challenge, which take cares of managing the challenges.
    
    It basically offer a sane & internal way to manage everything using a key-value pair
    without ever having to touch the challenges/captcha directly.
    """
    
    def __init__(self) -> None:
        self.queue: Dict[int, Challenge] = {}

    def create_challenge(self, id: int, **kwargs: Dict[Any, Any]) -> Challenge:
        """Create a challenge for an id. Overwrite the challenge created before, unless the 
        challenge is not fully completed.

        Parameters
        ----------
        id: int
            The id associated to the generated challenge.

        Returns
        -------
        Challenge:
            The generated challenge.
        """
        challenge = Challenge(**kwargs)
        self.queue[id] = challenge
        return challenge

    def get_challenge(self, id: int) -> Challenge:
        """Get the challenge of an id, if it exist.

        Parameters
        ----------
        id: int
            The id associated to the challenge.

        Returns
        -------
        Challenge:
            The challenge associated to the id.

        Raises
        ------
        UnexistingChallengeError:
            If the given id does not have any associated challenge, raise this error.
        """
        try:
            return self.queue[id]
        except KeyError as error:
            raise UnexistingChallengeError(f"Challenge for id '{error}' does not exist.") from None

    def delete_challenge(self, id: int):
        """Delete a challenge of an id, if it exist.

        Parameters
        ----------
        id: int
            The id associated to the challenge.

        Raises
        ------
        UnexistingChallengeError:
            If the given id does not have any associated challenge, raise this error.
        """
        # Raises an error if does not exist.
        self.get_challenge(id)
        del self.queue[id]

# CHALLENGES: Dict[int, Challenge] = {}

# def check_fonts(*fonts: Union[str, Path]) -> bool:
#     """
#     Ensure the given fonts are valid by loading the fonts directly to Pillow.

#     Returns
#     -------
#     Optional[]
#     """
#     for font in fonts:
#         if isinstance(font, Path):
#             font = font.absolute().as_posix()
#         try:
#             ImageFont.truetype(font)
#         except OSError:
#             return False
#     return True
