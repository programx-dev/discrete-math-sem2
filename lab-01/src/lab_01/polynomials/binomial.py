from fractions import Fraction

from lab_01.math_engine.matrix import Vector


def generate_binomial_coeffs(power_k: int, a: Fraction):
    """
    Генератор коэффициентов (x - a)^k от старшей степени к младшей.
    """
    current_coeff = Fraction(1)
    for deg in range(power_k, -1, -1):
        yield current_coeff
        current_coeff = current_coeff * (-a) * deg / (power_k - deg + 1)


def get_col(power_k: int, a: Fraction, max_degree_n: int) -> Vector:
    """
    Формирует вектор-столбец для матрицы системы.
    """
    vector = [Fraction(0)] * (max_degree_n + 1)

    for i, val in enumerate(generate_binomial_coeffs(power_k, a)):
        vector[power_k - i] = val

    return vector
