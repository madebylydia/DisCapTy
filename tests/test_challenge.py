import unittest
from typing import Type

from discapty.challenge import Challenge
from discapty.generators import BaseGenerator, WheezyGenerator


class TestChallenge(unittest.TestCase):
    def test_create_challenge_with_wrong_generator(self):
        """
        Attempt to create a Challenge object by supplying a generator that does not
        inherit from BaseGenerator. Raises an exception.
        """

        class MyGen:
            def generate(self, text: str) -> str:
                return "+".join(text)

        with self.assertRaisesRegex(
            TypeError, r"The generator must be a subclass of BaseGenerator"
        ):
            Challenge(MyGen)  # type: ignore

    def test_create_challenge(self):
        """
        Attempt to create a Challenge object.
        """
        gen = WheezyGenerator

        challenge = Challenge(gen, generator_settings={"width": 500, "height": 300})
        self.assertIsInstance(challenge.generator, WheezyGenerator)


if __name__ == "__main__":
    unittest.main()
