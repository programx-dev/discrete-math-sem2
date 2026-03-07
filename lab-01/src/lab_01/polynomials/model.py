# model.py

from fractions import Fraction


class Polynomial:
    """
    Представление многочленов.
    """

    __slots__ = {"coeffs"}

    def __init__(self, coeffs: list[Fraction]):
        """
        Создать представление многочлена на основе вектора коэффицентов, от младшего к старшему.
        """
        self.coeffs = coeffs

    def __str__(self) -> str:
        if all(c == 0 for c in self.coeffs):
            return "0"

        terms = []
        for deg, coeff in reversed(list(enumerate(self.coeffs))):
            if coeff == 0:
                continue

            # Формируем знак
            sign = " + " if coeff > 0 else " - "
            if not terms and coeff > 0:
                sign = ""
            elif not terms and coeff < 0:
                sign = "-"

            # Формируем коэффициент
            abs_coeff = abs(coeff)
            coeff_str = ""

            # Печать дроби
            if abs_coeff != 1 or deg == 0:
                coeff_str = (
                    str(abs_coeff.numerator)
                    if abs_coeff.denominator == 1
                    else str(abs_coeff)
                )

            # Формируем x^deg
            if deg == 0:
                var_str = ""
            elif deg == 1:
                var_str = "x"
            else:
                var_str = f"x^{deg}"

            terms.append(f"{sign}{coeff_str}{var_str}")

        return "".join(terms).strip()

    def __repr__(self):
        return f"Polynomial({self.coeffs})"
