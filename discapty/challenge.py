import uuid
from enum import Enum
from typing import Any, Dict, Optional, Type

from discapty.generators import BaseGenerator
from discapty.utils import random_code
from discapty.errors import TooManyRetriesError


class FailReason(Enum):
    TOO_MANY_RETRIES = "Too many retries"
    FATAL = "Internal error"


class States(Enum):
    PENDING = "Pending"
    WAITING = "Waiting"
    COMPLETED = "Completed"
    FAILED = "Failed"


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

    .. versionadded:: 2.0.0
    """

    def __init__(
        self,
        generator: Type[BaseGenerator],
        id: Optional[int] = None,
        *,
        generator_settings: Optional[Dict[str, Any]] = None,
        retries: int = 3,
        code: Optional[str] = None,
        code_length: int = 4,
    ) -> None:
        if not issubclass(generator, BaseGenerator):
            raise TypeError("The generator must be a subclass of BaseGenerator")

        self.generator: BaseGenerator = (
            generator(**generator_settings) if generator_settings else generator()
        )
        self.code: str = code or random_code(code_length)
        self.id: str = str(id or uuid.uuid4())

        self.retries: int = retries
        self.failures: int = 0

        self.state: States = States.PENDING
        self._fail_reason: Optional[FailReason] = None

    def _set_state(
        self,
        state: States,
        fail_reason: Optional[FailReason] = None,
    ):
        self.state = state
        if self.state == "failed" and fail_reason:
            self.fail_reason = FailReason(fail_reason)

    def begin(self):
        """
        Start the challenge.
        """
        if self.state != States.PENDING:
            raise ValueError("This challenge is already running.")
        self._set_state(States.PENDING)
        return self.generator.generate(self.code)

    def check(self, answer: str) -> bool:
        """
        Check the answer.
        """
        if answer != self.code:
            self.failures += 1
            if self.failures >= self.retries:
                self._set_state(States.FAILED, FailReason.TOO_MANY_RETRIES)
                raise TooManyRetriesError(self.fail_reason)
            return False
        else:
            self._set_state(States.COMPLETED)
            return True
