#  Copyright (c) 2022​-present - Predeactor - Licensed under the MIT License.
#  See the LICENSE file included with the file for more information about this project's
#   license.

import uuid
from enum import Enum
from typing import Any, Optional

from discapty.captcha import Captcha
from discapty.errors import TooManyRetriesError, AlreadyCompletedError, AlreadyRunningError
from discapty.generators import BaseGenerator
from discapty.utils import random_code


class FailReason(Enum):
    TOO_MANY_RETRIES = "Too many retries"
    CANCELLED = "Challenge has been cancelled"


class States(Enum):
    """
    An enum representing the different states of a challenge.

    Available states are:

    PENDING  : The challenge is waiting for beginning.
    WAITING  : The challenge is waiting for user's input.
    COMPLETED: The challenge has been completed.
    FAILED   : The challenge has been failed without trouble.
    FAILURE  : The challenge has been completed without user's input and in an unexpected way.
        (e.g. manually cancelled
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

    Parameters
    ----------
    generator : BaseGenerator
        The generator class to use.
        You cannot uses :py:obj:`BaseGenerator <discapty.generators.BaseGenerator>`
        directly, you must subclass it and implement the "generate" function first.

    challenge_id : Optional[int | str]
        The id of the challenge. Can be a string or an id.
        If none is supplied, a random `UUID`_ will be generated.

    retries : Optional[int]
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
        generator: BaseGenerator,
        challenge_id: Optional[str] = None,
        *,
        retries: Optional[int] = None,
        code: Optional[str] = None,
        code_length: Optional[int] = None,
    ) -> None:
        self.generator = generator

        self.code: str = code or random_code(code_length)
        self.challenge_id: str = str(challenge_id or uuid.uuid4())

        self.retries: int = retries or 3
        self.failures: int = 0
        self.attempted_tries: int = 0

        self.state: States = States.PENDING
        self._fail_reason: Optional[FailReason] = None

        self.__last_captcha_object: Optional[Any] = None

    def _set_state(
        self,
        state: States,
        fail_reason: Optional[FailReason] = None,
    ):
        self.state = state
        if self.state == States.FAILED and fail_reason:
            self.fail_reason = FailReason(fail_reason).value

    @property
    def _can_be_modified(self) -> bool:
        return self.state in (
            States.COMPLETED,
            States.PENDING,
            States.WAITING,
        )

    def _create_captcha(self) -> Captcha:
        """
        Create a new Captcha object.
        """
        generated_captcha = self.generator.generate(self.code)
        return Captcha(self.code, generated_captcha)

    def get_captcha(self, *, new: bool = False) -> Captcha:
        """
        Get the Captcha object.

        Parameters
        ----------
        new : bool
            If True, a new Captcha object will be created rather than using the one that was
            already generated, if applicable.
        """
        if new or (not self.__last_captcha_object):
            self.__last_captcha_object = self._create_captcha().captcha
        return self.__last_captcha_object

    @property
    def captcha(self) -> Captcha:
        return self.__last_captcha_object or self.get_captcha()

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
        """
        if self.state == States.FAILED:
            raise TooManyRetriesError(self.fail_reason)
        if self.state == States.COMPLETED:
            raise AlreadyCompletedError("Challenge already completed")
        if self.state == States.WAITING:
            raise AlreadyRunningError("Challenge is already being ran")

        self._set_state(States.PENDING)
        return self._create_captcha().captcha

    def check(self, answer: str, *, force_casing: bool = False, remove_space: bool = True) -> bool:
        """
        Check an answer.
        This will always add +1 to `attempted_tries`.

        Parameters
        ----------
        answer : str
            The answer to check against the Captcha's code.
        force_casing : bool
            If True, the casing must be respected.
        remove_space : bool
            If True, spaces will be removed when checking the answer.

        Return
        ------
        bool:
            True if the answer is correct, False otherwise.

        Raises
        ------
        :py:exc:`TooManyRetriesError`
            If the number of failures is greater than the number of retries allowed.
            We are still adding +1 to the failure even when raising the exception.
        """
        self.attempted_tries += 1

        if not self.captcha.check(answer, force_casing=force_casing, remove_space=remove_space):
            self.failures += 1
            if self.failures >= self.retries:
                self._set_state(States.FAILED, FailReason.TOO_MANY_RETRIES)
                raise TooManyRetriesError(self.fail_reason)
            return False
        else:
            self._set_state(States.COMPLETED)
            return True

    def cancel(self) -> None:
        """
        Cancel the challenge.
        """
        if self._can_be_modified:
            self._set_state(States.FAILURE, FailReason.CANCELLED)
