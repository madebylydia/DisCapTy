import typing
import uuid
from enum import Enum

from discapty.captcha import Captcha
from discapty.errors import (
    AlreadyCompletedError,
    AlreadyRunningError,
    ChallengeCompletionError,
    TooManyRetriesError,
)
from discapty.generators import Generator
from discapty.utils import random_code


class FailReason(Enum):
    """
    An enum with all possible reasons of failing the captcha.
    """

    TOO_MANY_RETRIES = "Too many retries"
    CANCELLED = "Challenge has been cancelled"


class States(Enum):
    """
    An enum representing the different states of a challenge.

    Available states are:

    * PENDING   : The challenge is waiting to begin.
    * WAITING   : The challenge is waiting for user's input.
    * COMPLETED : The challenge has been completed.
    * FAILED    : The challenge has been failed without trouble.
    * FAILURE   : The challenge has been completed without user's input and in an unexpected way. (e.g. manually cancelled)

    """

    PENDING = "Pending"
    WAITING = "Waiting"
    COMPLETED = "Completed"
    FAILED = "Failed"
    FAILURE = "Failure (Unexpected)"


_CR = typing.TypeVar("_CR")


class Challenge(typing.Generic[_CR]):
    """
    Representation of a challenge. A challenge represent the user's Captcha
    question-answer he must face.

    This class takes cares of:
        - Generating the captcha
        - Verify inputs
        - Manage the "Captcha" object

    It frees your mind from managing all the process of a captcha challenge, keeping
    your code short and easy.

    Parameters
    ----------
    generator : Subclass of :py:class:`discapty.generators.Generator`
        The generator class to use.

    challenge_id : Optional, :py:class:`str`
        The id of the challenge. Can be a string or an id.
        If none is supplied, a random :py:func:`UUID <uuid.uuid4>` will be generated.

    allowed_retries : Optional, :py:class:`int`
        The number of retries allowed. Defaults to 3.

    code : Optional, :py:class:`str`
        The code to use. If none is supplied, a random code will be generated.

    code_length : Optional, :py:class:`int`
        The length of the code to generate if no code is supplied. Defaults to 4.


    .. versionadded:: 2.0.0

    .. versionchanged:: 2.1.0

       This class is now a generic class and requires to indicate which type it will receive.
       (If necessary)
       If the type is not especially indicated in your variable, it should be automatically done.
    """

    generator: Generator[_CR]
    """
    The generator used with this challenge.
    """
    code: str
    """
    The clear code.
    """
    challenge_id: str
    """
    The ID of this challenge.
    """
    allowed_retries: int
    """
    The total allowed retried of this challenge.
    """
    failures: int
    """
    The total failures since this challenge has been created.
    """
    attempted_tries: int
    """
    The total attempted tried since this challenge has been created.
    """
    state: States
    """
    The actual state of the challenge.
    """
    fail_reason: typing.Optional[str]
    """
    The fail reason, if applicable.
    """
    __last_captcha_class: typing.Optional[Captcha[_CR]]
    __last_code: typing.Optional[str]

    def __init__(
        self,
        generator: Generator[_CR],
        challenge_id: typing.Optional[str] = None,
        *,
        allowed_retries: typing.Optional[int] = None,
        code: typing.Optional[str] = None,
        code_length: typing.Optional[int] = None,
    ) -> None:
        self.generator = generator

        self.code = code or random_code(code_length)
        self.challenge_id = str(challenge_id or uuid.uuid4())

        self.allowed_retries = allowed_retries or 3
        self.failures = 0
        self.attempted_tries = 0

        self.state = States.PENDING
        self.fail_reason = None

        self.__last_captcha_class = None
        self.__last_code = None

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"<Challenge id={self.challenge_id} state={self.state} "
            "is_completed={self.is_completed}>"
        )

    def _set_state(
        self,
        state: States,
        fail_reason: typing.Optional[FailReason] = None,
    ) -> None:
        self.state = state
        if (
            self.state
            in (
                States.FAILED,
                States.FAILURE,
            )
            and fail_reason
        ):
            self.fail_reason = fail_reason.value

    @property
    def _can_be_modified(self) -> bool:
        return self.state in (
            States.PENDING,
            States.WAITING,
        )

    def _create_captcha(self) -> Captcha[_CR]:
        if not self.__last_captcha_class or (self.code != self.__last_code):
            generated_captcha = self.generator.generate(self.code)
            self.__last_captcha_class = Captcha(self.code, generated_captcha)
            self.__last_code = self.code
        return self.__last_captcha_class

    @property
    def captcha_object(self) -> _CR:
        """
        Get the Captcha object.

        Returns
        -------
        :py:attr:`discapty.constants.GeneratorReturnType` :
            The Captcha object.
        """
        return self.captcha.captcha_object

    @property
    def captcha(self) -> Captcha[_CR]:
        """
        The Captcha class associated to this challenge.

        Returns
        -------
        :py:class:`discapty.captcha.Captcha` :
            The Captcha class.
        """
        return self._create_captcha()

    @property
    def is_completed(self) -> bool:  # pragma: no cover
        """
        Check if the challenge has been completed or failed.

        Returns
        -------
        :py:class:`bool` :
            If the challenge has been completed or failed.
        """
        return self.state in (States.COMPLETED, States.FAILED)

    @property
    def is_correct(self) -> typing.Optional[bool]:  # pragma: no cover
        """
        Check if the challenge has been completed. If not, return None. If failed, return False.

        Returns
        -------
        Optional, :py:class:`bool` :
            If the challenge has been completed with success. If not, return False. If not completed, return None.
        """
        return self.state == States.COMPLETED if self.is_completed else None

    @property
    def is_wrong(self) -> typing.Optional[bool]:  # pragma: no cover
        """
        Check if the challenge has been failed. If not, return None. If completed, return False.

        Returns
        -------
        Optional, :py:class:`bool` :
            If the challenge has been failed. If not, return False. If not completed, return None.

        """
        return self.state == States.FAILED if self.is_completed else None

    def begin(self) -> _CR:
        """
        Begins the challenge.

        Raises
        ------
        :py:exc:`AlreadyCompletedError` :
            If the challenge has already been completed. You cannot start a challenge twice,
            you need to create a new one.
        :py:exc:`AlreadyRunningError` :
            If the challenge is already running.
        :py:exc:`TooManyRetriesError` :
            If the number of failures is greater than the number of retries allowed.
            In other words, the challenge has failed.
        :py:exc:`ChallengeCompletionError` :
            If the challenge had a failure. Returns the failure's reason.

        Returns
        -------
        The Captcha object to send to the user.


        .. versionchanged:: 2.1.0

           The return type will now be dynamically acquired and adapt to the given generator.
        """
        if self.state == States.FAILED:
            reason = self.fail_reason or "Failed (No failed reason)"
            raise TooManyRetriesError(reason)
        if self.state == States.FAILURE:
            reason = self.fail_reason or "Failure (No failure reason)"
            raise ChallengeCompletionError(reason)
        if self.state == States.COMPLETED:
            raise AlreadyCompletedError("Challenge already completed")
        if self.state == States.WAITING:
            raise AlreadyRunningError("Challenge is already being ran")

        self._set_state(States.WAITING)
        return self.captcha_object

    def check(
        self, answer: str, *, force_casing: bool = False, remove_spaces: bool = True
    ) -> bool:
        """
        Check an answer.
        This will always add +1 to `attempted_tries` and `failures` if necessary.

        Parameters
        ----------
        answer : :py:class:`str`
            The answer to check against the Captcha's code.
        force_casing : :py:class:`bool`
            If True, the casing must be respected. Defaults to False.
        remove_spaces : :py:class:`bool`
            If True, spaces will be removed when checking the answer. Defaults to True.

        Raises
        ------
        :py:exc:`TooManyRetriesError` :
            If the number of failures is greater than the number of retries allowed.
            We are still adding +1 to the failure even when raising the exception.
        :py:exc:`TypeError` :
            The challenge cannot be edited (State is either not PENDING or not WAITING)

        Return
        ------
        :py:class:`bool` :
            True if the answer is correct, False otherwise.
        """
        if not self._can_be_modified:
            raise TypeError("Challenge cannot be edited")

        self.attempted_tries += 1

        if not self.captcha.check(answer, force_casing=force_casing, remove_spaces=remove_spaces):
            # If wrong
            self.failures += 1
            if self.failures >= self.allowed_retries:
                self._set_state(States.FAILED, FailReason.TOO_MANY_RETRIES)
                raise TooManyRetriesError(self.fail_reason)
            return False
        else:
            # If correct
            self._set_state(States.COMPLETED)
            return True

    def reload(
        self, *, increase_attempted_tries: bool = True, increase_failures: bool = False
    ) -> _CR:
        """
        Reload the Challenge and its code.

        This method will create a new random code + captcha object. It will also increase the
        attempted_tries counter if requested. By defaults, this behavior is executed.

        Parameters
        ----------
        increase_attempted_tries : :py:class:`bool`
            If True, the attempted_tries counter will be increased.

        increase_failures : :py:class:`bool`
            If True, the failures counter will be increased.

        Raises
        ------
        :py:exc:`TypeError` :
            If the challenge cannot be edited or is not already running.

        Returns
        -------
        :py:attr:`discapty.constants.GeneratorReturnType` :
            The Captcha object to send to the user.


        .. versionchanged:: 2.1.0
           The return type will now be dynamically acquired and adapt to the given generator.

        """
        if not self._can_be_modified:
            raise TypeError("Challenge cannot be edited")
        if self.state == States.PENDING:
            raise TypeError("Challenge is not running")

        self.code = random_code()

        if increase_attempted_tries:
            self.attempted_tries += 1
            if increase_failures:
                self.failures += 1

        return self.captcha_object

    def cancel(self) -> None:
        """
        Cancel the challenge.

        Raises
        ------
        :py:exc:`TypeError` :
            If the challenge cannot be edited.
        """
        if not self._can_be_modified:
            raise TypeError("Challenge cannot be edited")

        self._set_state(States.FAILURE, FailReason.CANCELLED)
