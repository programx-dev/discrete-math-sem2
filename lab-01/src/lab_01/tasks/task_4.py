# task_4.py

import sys
from enum import Enum
from fractions import Fraction
from typing import Union

from lab_01.math_engine.matrix import MatrixError
from lab_01.polynomials.horner import divmod_horner, get_quotient_degree
from lab_01.polynomials.model import Polynomial
from lab_01.polynomials.parser import parse_coeff_string


class InfinityType(Enum):
    POSITIVE = "+inf"
    NEGATIVE = "-inf"
    NEUTRAL = "inf"


def sgn(frac: Fraction) -> int:
    """
    Математичская функция sgn: 1, -1 или 0.
    """
    return (frac > 0) - (frac < 0)


def to_str(res: Union[Fraction, InfinityType]) -> str:
    if isinstance(res, InfinityType):
        if res == InfinityType.POSITIVE:
            return "+∞"
        if res == InfinityType.NEGATIVE:
            return "-∞"
        return "∞"
    # Форматирование дробей
    if res.numerator == 0:
        return "0"
    if res.denominator == 1:
        return str(res.numerator)
    return f"{res.numerator}/{res.denominator}"


def calculate_limit_at_A(
    f_vec: list[Fraction], g_vec: list[Fraction], A: Fraction
) -> InfinityType | Fraction:
    f1, n = get_quotient_degree(f_vec, A)
    g1, m = get_quotient_degree(g_vec, A)

    val_f1 = divmod_horner(f1, A)[1]
    val_g1 = divmod_horner(g1, A)[1]

    if n > m:
        return Fraction(0)

    if n == m:
        return val_f1 / val_g1

    k = m - n
    if k % 2 == 0:
        return (
            InfinityType.POSITIVE if sgn(val_f1 / val_g1) > 0 else InfinityType.NEGATIVE
        )
    else:
        return InfinityType.NEUTRAL


def calculate_limit_at_inf(
    f_vec: list[Fraction], g_vec: list[Fraction]
) -> tuple[InfinityType | Fraction, InfinityType | Fraction]:
    deg_f, deg_g = len(f_vec) - 1, len(g_vec) - 1
    f_lead, g_lead = f_vec[-1], g_vec[-1]

    if deg_f < deg_g:
        lim_pos_inf = lim_neg_inf = Fraction(0)
    elif deg_f == deg_g:
        lim_pos_inf = lim_neg_inf = f_lead / g_lead
    else:
        s_pos = sgn(f_lead / g_lead)
        lim_pos_inf = InfinityType.POSITIVE if s_pos > 0 else InfinityType.NEGATIVE

        s_neg = s_pos * ((-1) ** (deg_f - deg_g))
        lim_neg_inf = InfinityType.POSITIVE if s_neg > 0 else InfinityType.NEGATIVE

    return lim_pos_inf, lim_neg_inf


def main():
    print("=== Пределы рациональной функции f(x)/g(x) ===")
    try:
        f_vec = parse_coeff_string(input("Коэффициенты f(x) (x^0 x^1 ...): "))
        g_vec = parse_coeff_string(input("Коэффициенты g(x) (x^0 x^1 ...): "))
        A = Fraction(input("Введите точку A для предела x -> A: "))

        print(f"\nВаша функция: R(x) = ({Polynomial(f_vec)}) / ({Polynomial(g_vec)})")

        lim_A = calculate_limit_at_A(f_vec, g_vec, A)
        lim_pos_inf, lim_neg_inf = calculate_limit_at_inf(f_vec, g_vec)

        print(f"x → {A}:  {to_str(lim_A)}")
        print(f"x → +∞: {to_str(lim_pos_inf)}")
        print(f"x → -∞: {to_str(lim_neg_inf)}")
        print("========================================================\n")

    except (MatrixError, ValueError, KeyboardInterrupt) as e:
        print(f"\nОшибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
