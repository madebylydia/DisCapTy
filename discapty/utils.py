from random import SystemRandom
from string import ascii_uppercase, digits

ESCAPE_CHAR = "\u200B"
table = [i * 1.97 for i in range(256)]


def random_code(length: int = 8):
    return "".join(
        SystemRandom().choice(ascii_uppercase + digits) for _ in range(length)
    )
