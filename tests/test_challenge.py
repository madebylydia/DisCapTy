#  Copyright (c) 2022​-present - Predeactor - Licensed under the MIT License.
#  See the LICENSE file included with the file for more information about this project's
#   license.

import unittest

from discapty import (
    AlreadyCompletedError,
    AlreadyRunningError,
    Challenge,
    ChallengeCompletionError,
    States,
    TooManyRetriesError,
    WheezyGenerator,
)


class TestChallenge(unittest.TestCase):
    """
    Test the discapty.Challenge object.
    """

    def test_create_challenge(self):
        """
        Attempt to create a Challenge object.
        """
        challenge = Challenge(WheezyGenerator())
        self.assertIsInstance(challenge.generator, WheezyGenerator)

    def test_can_begin(self):
        """
        Attempt to begin the challenge.
        """
        challenge = Challenge(WheezyGenerator())
        challenge.begin()

        self.assertIs(challenge.state, States.WAITING)

    def test_can_not_begin(self):
        """
        Check that the challenge cannot begin.
        """
        challenge = Challenge(WheezyGenerator())
        challenge.state = States.FAILED
        self.assertRaises(TooManyRetriesError, challenge.begin)

        challenge.state = States.FAILURE
        self.assertRaises(ChallengeCompletionError, challenge.begin)

        challenge.state = States.COMPLETED
        self.assertRaises(AlreadyCompletedError, challenge.begin)

        challenge.state = States.WAITING
        self.assertRaises(AlreadyRunningError, challenge.begin)

    def test_can_be_reloaded(self):
        """
        Try to reload the Challenge's code.
        """
        challenge = Challenge(WheezyGenerator(width=500, height=300), code="wheezy")

        with self.assertRaisesRegex(TypeError, "Challenge is not running"):
            challenge.reload()

        challenge.begin()
        challenge.reload()
        self.assertEqual(challenge.attempted_tries, 1)
        self.assertNotEqual(challenge.code, "wheezy")

        challenge.reload(increase_attempted_tries=False)
        self.assertEqual(challenge.attempted_tries, 1)

    def test_ensure_captcha_is_same(self):
        """
        Ensure that the same captcha is generated each time.
        """
        challenge = Challenge(WheezyGenerator(width=500, height=300))
        first = challenge.captcha_object
        second = challenge.captcha_object
        self.assertEqual(id(first), id(second))

        challenge.code = "Anything goes!"
        third = challenge.captcha_object
        self.assertNotEqual(id(first), id(third))

    def test_challenge_validation(self):
        """
        Ensure that the Challenge returns the correct boolean when checking codes.
        """
        challenge = Challenge(WheezyGenerator(width=500, height=300), code="wheezy")

        # Testing an incorrect code
        self.assertFalse(challenge.check("whezzy"))
        self.assertIs(challenge.failures, 1)
        self.assertIs(challenge.attempted_tries, 1)

        # Testing correct code
        self.assertTrue(challenge.check("wheezy"))
        self.assertIs(challenge.failures, 1)
        self.assertIs(challenge.state, States.COMPLETED)

    def test_ensure_failures(self):  # sourcery skip: class-extract-method
        """
        Ensure that the challenge raises an error if too many fails.
        """
        challenge = Challenge(WheezyGenerator())
        challenge.begin()

        # Testing an incorrect code
        for _ in range(challenge.allowed_retries - 1):
            challenge.check("random")

        with self.assertRaises(TooManyRetriesError):
            challenge.check("random")

    def test_ensure_last_failure(self):
        """
        Ensure that the challenge can handle a last success before failure.
        """
        challenge = Challenge(WheezyGenerator())
        challenge.begin()

        # Testing an incorrect code
        for _ in range(challenge.allowed_retries - 1):
            challenge.check("random")

        self.assertTrue(challenge.check(challenge.code))

    def test_increase_attempted_tries_on_reload(self):
        """
        Ensure the challenge increases the failure by one if specified.
        """
        challenge = Challenge(WheezyGenerator())
        challenge.begin()
        actual_tries = challenge.attempted_tries
        challenge.reload(increase_attempted_tries=True)

        self.assertGreater(challenge.attempted_tries, actual_tries)

    def test_increase_failure_on_reload(self):
        """
        Ensure the challenge increases the failure by one if specified.
        """
        challenge = Challenge(WheezyGenerator())
        challenge.begin()
        actual_failures = challenge.failures
        challenge.reload(increase_failures=True)

        self.assertGreater(challenge.failures, actual_failures)

    def test_cant_reload_on_failed(self):
        """
        Ensure the challenge can't be modified on reload.
        """
        challenge = Challenge(WheezyGenerator())
        challenge.state = States.FAILED

        self.assertRaises(TypeError, challenge.reload)

    def test_cant_check(self):
        """
        Ensure the challenge cannot be checked if not modifiable
        """
        challenge = Challenge(WheezyGenerator())
        challenge.state = States.FAILED
        
        self.assertRaises(TypeError, challenge.check)

    def test_cant_cancel(self):
        """
        Ensure the challenge cannot be cancelled if not modifiable
        """
        challenge = Challenge(WheezyGenerator())
        challenge.state = States.FAILED
        
        self.assertRaises(TypeError, challenge.cancel)

    def test_casing_enforcement(self):
        """
        Ensure that the casing is respected.
        """
        challenge = Challenge(WheezyGenerator(), code="TEST")
        challenge.begin()

        self.assertFalse(challenge.check("test", force_casing=True))
        self.assertTrue(challenge.check("test", force_casing=False))

    def test_spaces_removal(self):
        """
        Ensure that spaces are removed if needed.
        """
        challenge = Challenge(WheezyGenerator(), code="TEST")
        challenge.begin()

        self.assertFalse(challenge.check("TE ST", remove_spaces=False))
        self.assertTrue(challenge.check("TE ST", remove_spaces=True))


if __name__ == "__main__":
    unittest.main()
