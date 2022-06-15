#  Copyright (c) 2022​-present - Predeactor - Licensed under the MIT License.
#  See the LICENSE file included with the file for more information about this project's
#   license.

# noinspection PyUnresolvedReferences
from pydantic.color import Color as Color

from .captcha import Captcha as Captcha
from .captcha_queue import CaptchaQueue as CaptchaQueue
from .challenge import Challenge as Challenge
from .challenge import States as States
from .errors import *
from .generators import Generator as Generator
from .generators import ImageGenerator as ImageGenerator
from .generators import TextGenerator as TextGenerator
from .generators import WheezyGenerator as WheezyGenerator

# DisCapTy: Version 2.0 - Release Candidate 1
__version__ = "2.0rc1"
