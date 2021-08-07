class CopyPasteError(Exception):
    """
    An error raised if the user sent the exact same code of the generated code when using a
    PlainCaptcha captcha type.
    """

    pass
