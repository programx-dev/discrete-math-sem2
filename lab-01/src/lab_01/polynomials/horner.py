# horner.py

from fractions import Fraction

from lab_01.math_engine.matrix import Vector


def horner(f: Vector, a: Fraction) -> tuple[Vector, Fraction]:
    quotient = [Fraction(0)] * len(f)
    quotient[-1] = f[-1]

    for i in range(len(f) - 2, -1, -1):
        quotient[i] = a * quotient[i + 1] + f[i]

    return quotient[1:], quotient[0]