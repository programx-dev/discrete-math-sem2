# parser.py

from fractions import Fraction

from lab_01.math_engine.matrix import Vector


def parse_coeff_string(input_str: str) -> Vector:
    """
    Преобразует строку коэффициентов в список Fraction.
    Пример: "1 0.5 -1/3" -> [Fraction(1, 1), Fraction(1, 2), Fraction(-1, 3)].
    """
    tokens = input_str.strip().split()

    coeffs = []
    for t in tokens:
        try:
            coeffs.append(Fraction(t))
        except ValueError:
            raise ValueError(f"Ошибка: '{t}' не является валидным числом или дробью.")

    return coeffs


def align_polynomials(all_coeffs: list[Vector]) -> list[Vector]:
    """
    Дополнить незначащями нулями векторы коэффицентов до одинаковой размерности.
    """
    if not all_coeffs:
        return []

    # Находим максимальную степень
    max_len = max(len(c) for c in all_coeffs)

    # Дополняем каждый список нулями в конец
    aligned = []
    for coeffs in all_coeffs:
        padded = coeffs + [Fraction(0)] * (max_len - len(coeffs))
        aligned.append(padded)

    return aligned
