#  Copyright (c) 2022​-present - Predeactor - Licensed under the MIT License.
#  See the LICENSE file included with the file for more information about this project's
#   license.

import random
import typing

from discapty.challenge import Challenge
from discapty.errors import NonexistingChallengeError
from discapty.generators import Generator


class CaptchaQueue:
    """
    A safe handler for taking cares of managing the challenges for the developer.

    It basically offers a sane & internal way to manage your captcha using a key-value pair
    without ever having to touch the challenges/captcha directly.

    Parameters
    ----------
    generators: Union[Generator, typing.List[Generator]]
        A list or a single generator to use for creating the challenges.
        If a list is given, a random generator will be picked up when using `create_challenge`.

        You should be aware that inconsistency will occur this way, as if one generator can return
        a specific type and another one could return another kind of type.

    queue: typing.Dict[str, Challenge]
        Import an existing queue. Shouldn't be required.

    Raises
    ------
    ValueError
        If no generators has been passed.
    """

    def __init__(
        self,
        generators: typing.Union[Generator, typing.List[Generator]],
        *,
        queue: typing.Optional[typing.Dict[str, Challenge]] = None,
    ) -> None:
        self.generators: typing.List[Generator] = []
        if isinstance(generators, list):
            self.generators.extend(generators)
        else:
            self.generators.append(generators)

        self.queue: typing.Dict[str, Challenge] = queue or {}
        self.__total_challenges: int = 0

    def create_challenge(
        self,
        challenge_id: typing.Optional[str] = None,
        *,
        retries: typing.Optional[int] = None,
        code: typing.Optional[str] = None,
        code_length: typing.Optional[int] = None,
    ) -> Challenge:
        """Create a challenge for an id. Overwrite the challenge created before, unless the
        challenge is not fully completed.

        Parameters
        ----------
        challenge_id: str
            The id associated to the challenge. If not given, a random id will be generated.
        retries: int
            The number of allowed retries. Defaults to 3.
        code: str
            The code to use. Defaults to a random code.
        code_length: int
            The length of the code to generate if no code is supplied. Defaults to 4.

        Returns
        -------
        Challenge:
            The generated challenge.
        """
        challenge_id = challenge_id or str(self.__total_challenges)

        random_generator = random.choice(self.generators)
        challenge = Challenge(
            random_generator,
            challenge_id,
            allowed_retries=retries,
            code=code,
            code_length=code_length,
        )
        self.queue[str(challenge_id)] = challenge

        self.__total_challenges += 1
        return challenge

    def get_challenge(self, challenge_id: str) -> Challenge:
        """Get the challenge of an id, if it exist.

        Parameters
        ----------
        challenge_id: str
            The id associated to the challenge.

        Returns
        -------
        Challenge:
            The challenge associated to the id.

        Raises
        ------
        :py:exc:`~errors.UnexistingChallengeError`:
            If the given id does not have any associated challenge.
        """
        try:
            return self.queue[challenge_id]
        except KeyError as e:
            raise NonexistingChallengeError(
                f"Challenge with id '{challenge_id}' does not exist. Have you used an int?"
            ) from e

    def delete_challenge(self, challenge_id: str) -> None:
        """Delete a challenge of an id, if it exist.

        Parameters
        ----------
        challenge_id: int
            The id associated to the challenge.

        Raises
        ------
        :py:exc:`~errors.UnexistingChallengeError`:
            If the given id does not have any associated challenge.
        """
        challenge = self.get_challenge(challenge_id)
        challenge.cancel()
        del self.queue[challenge_id]
