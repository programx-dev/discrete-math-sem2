# horner.py
from fractions import Fraction
from lab_01.math_engine.matrix import Vector
from lab_01.polynomials.parser import strip_trailing_zeros


def divmod_horner(f: Vector, A: Fraction) -> tuple[Vector, Fraction]:
    """
    Получить неполное частное и остаток от деления многочлена на (x - A).
    """
    quotient = [Fraction(0)] * len(f)
    quotient[-1] = f[-1]

    for i in range(len(f) - 2, -1, -1):
        quotient[i] = A * quotient[i + 1] + f[i]

    return quotient[1:] or [Fraction(0)], quotient[0]


def get_quotient_degree(f: Vector, A: Fraction) -> tuple[Vector, int]:
    """
    Выделяет множитель (x - A)^n.
    Возвращает (f1, n), где f(x) = (x - A)^n * f1(x) и f1(A) != 0.
    """
    n = 0
    current_f = strip_trailing_zeros(f)

    while len(current_f) > 0:
        q, mod = divmod_horner(current_f, A)
        if mod != 0:
            break

        n += 1
        current_f = q

        if not any(current_f):
            break

    return current_f, n
