from typing import Dict, List

sequence = tuple(t / 20.0 for t in range(21))
beziers: Dict[int, List[List[float]]] = {}


def pascal_row(n: int) -> List[int]:
    """Returns n-th row of Pascal's triangle"""
    result = [1]
    x, numerator = 1, n
    for denominator in range(1, n // 2 + 1):
        x *= numerator
        x = int(x / denominator)
        result.append(x)
        numerator -= 1
    if n & 1 == 0:
        result.extend(reversed(result[:-1]))
    else:
        result.extend(reversed(result))
    return result


def make_bezier(n: int) -> List[List[float]]:
    """Bezier curves:
    http://en.wikipedia.org/wiki/B%C3%A9zier_curve#Generalization
    """
    try:
        return beziers[n]
    except KeyError:
        combinations = pascal_row(n - 1)
        result: List[List[float]] = []
        for t in sequence:
            power = (t**i for i in range(n))
            powers = ((1 - t) ** i for i in range(n - 1, -1, -1))
            coefficient = [c * a * b for c, a, b in zip(combinations, power, powers)]
            result.append(coefficient)
        beziers[n] = result
        return result
