from abc import ABC, abstractmethod
from io import BytesIO
from typing import Literal, Optional, TypedDict, Union

import discord

AVAILABLE_CAPTCHA_TYPES = Literal["image", "wheezy", "text"]


class Author(TypedDict):
    name: str
    url: str


class Footer(TypedDict):
    text: str
    url: str


class Captcha(ABC):
    def __init__(self) -> None:
        self.code: str
        self.type: AVAILABLE_CAPTCHA_TYPES

    @abstractmethod
    async def generate(self):
        raise NotImplementedError()

    @abstractmethod
    def to_embed(
        self,
        guild_name: str,
        *,
        author: Optional[Author] = None,
        footer: Optional[Footer] = None,
        **kwargs,
    ) -> discord.Embed:
        raise NotImplementedError()

    @abstractmethod
    def get_discord_file(self):
        raise NotImplementedError()

    @abstractmethod
    def is_correct(self, code_to_validate: str):
        raise NotImplementedError()


class CaptchaGen(ABC):
    @abstractmethod
    def generate(self, code_to_generate: str, **kwargs) -> Union[BytesIO, str]:
        raise NotImplementedError()
