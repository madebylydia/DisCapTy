import typing

GeneratorReturnType = typing.TypeVar("GeneratorReturnType", covariant=True)
"""
Return type of the generator.
"""

CaptchaReturnType = typing.TypeVar("CaptchaReturnType")
"""
Return type of the Captcha object.
"""
