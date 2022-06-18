#  Copyright (c) 2022​-present - Predeactor - Licensed under the MIT License.
#  See the LICENSE file included with the file for more information about this project's
#   license.

import unittest

import PIL.Image

from discapty.generators import Generator, ImageGenerator, TextGenerator, WheezyGenerator


class TestGenerator(unittest.TestCase):
    """
    Test the discapty.generators.Generator object.
    """

    given_input = "WORK"
    expected_output = "W+O+R+K"

    def test_create_generator(self):
        """
        Attempt to create a generator well-built with the correct parameters.
        """

        class MyGen(Generator):
            sep: str = "-"

            def generate(self, text: str):
                return self.sep.join(text)

        output = MyGen(sep="+").generate(self.given_input)
        self.assertEqual(output, self.expected_output)


class TestTextGenerator(unittest.TestCase):
    def test_generate_text(self):
        """
        Test the generate method of TextGenerator.
        """
        text = "WORK"
        expected_output = r"W+O+R+K"

        output = TextGenerator(separator="+").generate(text)
        self.assertEqual(output, expected_output)

    def test_generate_text_with_separator_list(self):
        """
        Test the generate method of TextGenerator that contains a list as separator.
        """
        text = "WORK"
        expected_output = r"W\+|-O\+|-R\+|-K"

        output = TextGenerator(separator=["+", "-"]).generate(text)
        self.assertRegex(output, expected_output)


class TestWheezyGenerator(unittest.TestCase):
    def test_create_wheezy_gen(self):
        """
        Attempt to create a Wheezy generator with the all parameters.
        """
        gen = WheezyGenerator(
            fonts_size=(50,),
            width=300,
            height=125,
            background_color="#EEEECC",
            text_color="#5C87B2",
            text_squeeze_factor=0.8,
            noise_number=30,
            noise_color="#EEEECC",
            noise_level=2,
        )
        result = gen.generate("TEST")

        self.assertIsInstance(result, PIL.Image.Image)


class TestImageGenerator(unittest.TestCase):
    def test_create_image_gen(self):
        """
        Attempt to create an Image generator with the all parameters.
        """
        gen = ImageGenerator(
            fonts_size=(50,),
            width=300,
            height=125,
            background_color="#EEEECC",
            text_color="#5C87B2",
            number_of_curves=2,
            number_of_dots=2,
            width_of_dots=2,
        )
        result = gen.generate("TEST")

        self.assertIsInstance(result, PIL.Image.Image)


if __name__ == "__main__":
    unittest.main()
