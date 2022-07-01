#  Copyright (c) 2022​-present - Predeactor - Licensed under the MIT License.
#  See the LICENSE file included with the file for more information about this project's
#   license.

import uuid
from enum import Enum
from typing import Any, Optional

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


class Challenge:
    """
    Representation of a challenge. A challenge represent the user's Captcha
    question-answer he must face.

    This class takes cares of:
        - Generating the captcha
        - Verify inputs
        - Manage the "Captcha" object

    It frees your mind from managing all the process of a captcha challenge, keeping
    your code short and easy.

    .. py:property:: code
        :type: str

        The raw code of the Challenge.

    .. py:property:: allowed_retries
        :type: int

        The number of allowed retries.

    .. py:property:: failures
        :type: int

        The number of failures the user has realized.

    .. py:property:: attempted_tries
        :type: int

        The number of tries the user has attempted. (Or how many time was ``.begin`` called)

    .. py:property:: state
        :type: discapty.States

        The current state of the challenge.

    .. py:property:: fail_reason
        :type: str

        The reason why the challenge has failed. Only filled if the state is failed or failure.

    Parameters
    ----------
    generator : Generator
        The generator class to use.
        You cannot uses :py:obj:`discapty.generators.Generator`
        directly, you have to subclass it and implement the "generate" function first.

    challenge_id : Optional[str]
        The id of the challenge. Can be a string or an id.
        If none is supplied, a random `UUID`_ will be generated.

    allowed_retries : Optional[int]
        The number of retries allowed. Defaults to 3.

    code : Optional[str]
        The code to use. If none is supplied, a random code will be generated.

    code_length : int
        The length of the code to generate if no code is supplied. Defaults to 4.


    .. versionadded:: 2.0.0

    .. _UUID: https://docs.python.org/3/library/uuid.html#uuid.uuid4
    """

    def __init__(
        self,
        generator: Generator,
        challenge_id: Optional[str] = None,
        *,
        allowed_retries: Optional[int] = None,
        code: Optional[str] = None,
        code_length: Optional[int] = None,
    ) -> None:
        self.generator = generator

        self.code: str = code or random_code(code_length)
        self.challenge_id: str = str(challenge_id or uuid.uuid4())

        self.allowed_retries: int = allowed_retries or 3
        self.failures: int = 0
        self.attempted_tries: int = 0

        self.state: States = States.PENDING
        self.fail_reason: Optional[FailReason] = None

        self.__last_captcha_class: Optional[Captcha] = None
        self.__last_code: Optional[str] = None

    def __repr__(self) -> str:
        return (
            f"<Challenge id={self.challenge_id} state={self.state} "
            "is_completed={self.is_completed}>"
        )

    def _set_state(
        self,
        state: States,
        fail_reason: Optional[FailReason] = None,
    ):
        """
        Set challenge's internal state.
        """
        self.state = state
        if (
            self.state
            in (
                States.FAILED,
                States.FAILURE,
            )
            and fail_reason
        ):
            self.fail_reason = FailReason(fail_reason).value

    @property
    def _can_be_modified(self) -> bool:
        """
        Check if the challenge can be modified.
        """
        return self.state in (
            States.PENDING,
            States.WAITING,
        )

    def _create_captcha(self) -> Captcha:
        """
        Create a new Captcha object.

        This will return a cached Captcha if the code hasn't changed.
        """
        if not self.__last_captcha_class or (self.code != self.__last_code):
            generated_captcha = self.generator.generate(self.code)
            self.__last_captcha_class = Captcha(self.code, generated_captcha)
            self.__last_code = self.code
        return self.__last_captcha_class

    @property
    def captcha_object(self) -> Any:
        """
        Get the Captcha object.

        Returns
        -------
        :py:obj:`typing.Any`
            The Captcha object.
        """
        return self.captcha.captcha_object

    @property
    def captcha(self) -> Captcha:
        """
        Returns the Captcha class associated to this challenge.
        """
        return self._create_captcha()

    @property
    def is_completed(self) -> bool:
        """
        Check if the challenge has been completed or failed.
        """
        return self.state in (States.COMPLETED, States.FAILED)

    @property
    def is_correct(self) -> Optional[bool]:
        """
        Check if the challenge has been completed. If not, return None. If failed, return False.
        """
        return self.state == States.COMPLETED if self.is_completed else None

    @property
    def is_wrong(self) -> Optional[bool]:
        """
        Check if the challenge has been failed. If not, return None. If completed, return False.
        """
        return self.state == States.FAILED if self.is_completed else None

    def begin(self) -> Any:
        """
        Start the challenge.

        Returns
        -------
        Captcha
            The Captcha object to send to the user.

        Raises
        ------
        :py:exc:`AlreadyCompletedError`
            If the challenge has already been completed. You cannot start a challenge twice,
            you need to create a new one.
        :py:exc:`AlreadyRunningError`
            If the challenge is already running.
        :py:exc:`TooManyRetriesError`
            If the number of failures is greater than the number of retries allowed.
            In other words, the challenge has failed.
        :py:exc:`ChallengeCompletionError`
            If the challenge had a failure. Returns the failure's reason.
        """
        if self.state == States.FAILED:
            raise TooManyRetriesError(self.fail_reason)
        if self.state == States.FAILURE:
            raise ChallengeCompletionError(self.fail_reason)
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
        answer : str
            The answer to check against the Captcha's code.
        force_casing : bool
            If True, the casing must be respected. Defaults to False.
        remove_spaces : bool
            If True, spaces will be removed when checking the answer. Defaults to True.

        Return
        ------
        bool:
            True if the answer is correct, False otherwise.

        Raises
        ------
        :py:exc:`TooManyRetriesError`
            If the number of failures is greater than the number of retries allowed.
            We are still adding +1 to the failure even when raising the exception.
        :py:exc:`TypeError`
            The challenge cannot be edited (State is either not PENDING or not WAITING)
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
    ) -> Any:
        """
        Reload the Challenge and its code.

        This method will create a new random code. It will also increase the attempted_tries
        counter if requested. By defaults, this behavior is executed.

        Parameters
        ----------
        increase_attempted_tries : bool
            If True, the attempted_tries counter will be increased.

        increase_failures : bool
            If True, the failures counter will be increased.

        Raises
        ------
        TypeError
            If the challenge cannot be edited or is not already running.
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
        TypeError:
            If the challenge cannot be edited.
        """
        if not self._can_be_modified:
            raise TypeError("Challenge cannot be edited")

        self._set_state(States.FAILURE, FailReason.CANCELLED)
