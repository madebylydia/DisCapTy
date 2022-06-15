#  Copyright (c) 2022​-present - Predeactor - Licensed under the MIT License.
#  See the LICENSE file included with the file for more information about this project's
#   license.

import unittest

from discapty.challenge import Challenge
from discapty.generators import WheezyGenerator


class TestChallenge(unittest.TestCase):
    """
    Test the discapty.Challenge object.
    """

    def test_create_challenge_with_wrong_generator(self):
        """
        Attempt to create a Challenge object by supplying a generator that does not
        inherit from Generator. Raises an exception.
        """

        class MyGen:
            def generate(self, text: str) -> str:
                return "+".join(text)

        with self.assertRaisesRegex(TypeError, r"The generator must be a subclass of Generator"):
            Challenge(MyGen)  # type: ignore

    def test_create_challenge(self):
        """
        Attempt to create a Challenge object.
        """
        challenge = Challenge(WheezyGenerator(width=500, height=300))
        self.assertIsInstance(challenge.generator, WheezyGenerator)

    def test_ensure_captcha_is_same(self):
        """
        Ensure that the same captcha is generated each time.
        """
        challenge = Challenge(WheezyGenerator(width=500, height=300))
        first = challenge.get_captcha()
        second = challenge.get_captcha()
        self.assertEqual(id(first), id(second))

        third = challenge.get_captcha(new=True)
        self.assertNotEqual(id(first), id(third))


if __name__ == "__main__":
    unittest.main()
