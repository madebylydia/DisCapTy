import random
import typing

from discapty.challenge import Challenge
from discapty.errors import NonexistingChallengeError
from discapty.generators import Generator

_GR = typing.TypeVar("_GR", covariant=True)


class CaptchaQueue(typing.Generic[_GR]):
    """
    A safe handler for taking cares of managing the challenges for the developer.

    It basically offers a sane & internal way to manage your captcha using a key-value pair
    without ever having to touch the challenges/captcha directly.

    Parameters
    ----------
    generators : :py:class:`discapty.generators.Generator` or list of :py:class:`discapty.generators.Generator`
        A list or a single generator to use for creating the challenges.
        If a list is given, a random generator will be picked up when using :py:func:`create_challenge <discapty.captcha_queue.CaptchaQueue.create_challenge>`.

        You should be aware that inconsistency will occur this way, as if one generator can return
        a specific type and another one could return another kind of type.

    queue : Dict[:py:class:`str`, :py:class:`discapty.challenge.Challenge`]
        Import an existing queue. Shouldn't be required.

    Raises
    ------
    :py:exc:`ValueError` :
        If no generators has been passed.


    .. versionadded:: 2.0.0

    .. versionchanged:: 2.1.0

       This class is now a generic class and requires to indicate which type it will receive.
       (If necessary)
       If the type is not especially indicated in your variable, it should be automatically done.

    """

    generators: typing.List[Generator[_GR]]
    queue: typing.Dict[str, Challenge[_GR]]
    __total_challenges: int

    def __init__(
        self,
        generators: typing.Union[
            Generator[_GR],
            typing.Iterable[Generator[_GR]],
        ],
        *,
        queue: typing.Optional[typing.Dict[str, Challenge[_GR]]] = None,
    ) -> None:
        self.generators = []
        if isinstance(generators, Generator):
            self.generators.append(generators)
        else:
            self.generators.extend(iter(generators))
        self.queue = queue or {}
        self.__total_challenges = 0

    def create_challenge(
        self,
        challenge_id: typing.Optional[str] = None,
        *,
        retries: typing.Optional[int] = None,
        code: typing.Optional[str] = None,
        code_length: typing.Optional[int] = None,
    ) -> Challenge[_GR]:
        """
        Create a challenge for an id. Overwrite the challenge created before, unless the
        challenge is not fully completed.

        Parameters
        ----------
        challenge_id : Optional, :py:class:`str`
            The id associated to the challenge. If not given, a random id will be generated.
        retries : Optional, :py:class:`int`
            The number of allowed retries. Defaults to 3.
        code : Optional, :py:class:`str`
            The code to use. Defaults to a random code.
        code_length : Optional, :py:class:`int`
            The length of the code to generate if no code is supplied. Defaults to 4.

        Returns
        -------
        :py:class:`discapty.challenge.Challenge` :
            The generated challenge.


        .. versionchanged:: 2.1.0

           The return type will now be dynamically acquired and adapt to the given generator(s).
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

    def get_challenge(self, challenge_id: str) -> Challenge[_GR]:
        """
        Get the challenge of an id, if it exist.

        Parameters
        ----------
        challenge_id : :py:class:`str`
            The id associated to the challenge.

        Raises
        ------
        :py:exc:`~errors.UnexistingChallengeError`:
            If the given id does not have any associated challenge.

        Returns
        -------
        :py:class:`discapty.challenge.Challenge` :
            The challenge associated to the id.


        .. versionchanged:: 2.1.0

           The return type will now be dynamically acquired and adapt to the given generator(s).

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
        challenge_id: :py:class:`int`
            The id associated to the challenge.

        Raises
        ------
        :py:exc:`~errors.UnexistingChallengeError`:
            If the given id does not have any associated challenge.
        """
        challenge = self.get_challenge(challenge_id)
        challenge.cancel()
        del self.queue[challenge_id]
