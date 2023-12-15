import unittest

import discapty
from discapty import CaptchaQueue, Challenge
from discapty.generators import TextGenerator, WheezyGenerator


class TestCaptchaQueue(unittest.TestCase):
    def setUp(self) -> None:
        self.queue: CaptchaQueue[str] = CaptchaQueue(TextGenerator())

    def test_create_queue_with_missing_gen(self):
        """
        Attempt to create a queue and fail because of missing generator(s)
        """
        with self.assertRaises(TypeError):
            CaptchaQueue()  # type: ignore

    def test_create_queue(self):
        """
        Attempt to create a queue.
        """
        self.assertIsInstance(self.queue, CaptchaQueue)

    def test_create_queue_with_multiple_generators(self):
        self.assertIsInstance(
            CaptchaQueue([TextGenerator(), WheezyGenerator()]), CaptchaQueue  # pyright: ignore[reportGeneralTypeIssues]
        )

    def test_create_challenge(self):
        """
        Attempt to create a challenge.
        """
        challenge = self.queue.create_challenge()

        self.assertIsInstance(challenge, Challenge)
        self.assertEqual(challenge.challenge_id, "0")

    def test_create_challenge_with_id(self):
        """
        Attempt to create a challenge with a given id.
        """
        given_id = "123"
        challenge = self.queue.create_challenge(given_id)

        self.assertEqual(challenge.challenge_id, given_id)

    def test_get_challenge(self):
        """
        Attempt to obtain a challenge directly through `self.queue.get_challenge`
        """
        created_challenge = self.queue.create_challenge()
        challenge = self.queue.get_challenge(created_challenge.challenge_id)

        self.assertEqual(id(challenge), id(created_challenge))

    def test_delete_nonexisting_challenge(self):
        """
        Attempt to delete a challenge that does not exist.
        """
        with self.assertRaises(discapty.NonexistingChallengeError):
            self.queue.delete_challenge("123")

    def test_delete_challenge(self):
        """
        Attempt to delete a challenge directly.
        """
        challenge_id = self.queue.create_challenge().challenge_id

        self.queue.delete_challenge(challenge_id)

        self.assertNotIn(challenge_id, self.queue.queue)
