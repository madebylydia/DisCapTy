import unittest

from discapty.captcha import Captcha


class TestCaptcha(unittest.TestCase):
    """
    Test the discapty.Challenge object.
    """

    def setUp(self):
        self.captcha = Captcha("TEST", "TeSt")

    def test_create_captcha_class(self):
        """
        Attempt to create a Captcha class manually.
        """
        # https://youtu.be/n6Xe3_TlL1o
        self.assertIsInstance(self.captcha, Captcha)

        self.assertIsInstance(self.captcha.captcha_object, str)

    def test_casing_enforcement(self):
        """
        Ensure that the casing is respected.
        """
        self.assertFalse(self.captcha.check("test", force_casing=True))
        self.assertTrue(self.captcha.check("test", force_casing=False))

    def test_spaces_removal(self):
        """
        Ensure that spaces are removed if needed.
        """
        self.assertFalse(self.captcha.check("TE ST", remove_spaces=False))
        self.assertTrue(self.captcha.check("TE ST", remove_spaces=True))
