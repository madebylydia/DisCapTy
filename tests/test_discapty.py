import unittest
import discapty

SEMANTIC_VERSION_REGEX = r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"

class TestRunner(unittest.TestCase):

    def test_version_respect_semantic(self):
        """
        Check if version respect semantic version.
        """
        self.assertRegex(discapty.__version__, SEMANTIC_VERSION_REGEX)

    @unittest.skip('Will test later')
    def test_create_captcha(self):
        """
        Attempt to create a captcha.
        """
        discapty.Captcha()

    @unittest.skip('Will test later')
    def test_create_challenge(self):
        """
        Attempt to create a challenge.
        """
        discapty.Challenge(
            code="My code",
            id=55247
        )

if __name__ == "__main__":
    unittest.main()
