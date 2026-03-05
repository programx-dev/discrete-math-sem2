# parser.py

from fractions import Fraction

from lab_01.math_engine.matrix import Vector


def strip_trailing_zeros(coeffs: list[Fraction]) -> list[Fraction]:
    """
    Удаляет незначащие нули в конце списка (старшие степени).
    """
    while len(coeffs) > 1 and coeffs[-1] == 0:
        coeffs.pop()

    return coeffs


def parse_coeff_string(input_str: str) -> list[Fraction]:
    """
    Преобразует строку коэффициентов в список Fraction без лишних нулей.
    """
    tokens = input_str.strip().split()

    if not tokens:
        return []

    coeffs = []
    for t in tokens:
        try:
            coeffs.append(Fraction(t))
        except ValueError:
            raise ValueError(f"Ошибка: '{t}' не является числом.")

    # Чистим вектор от лишних нулей в конце
    return strip_trailing_zeros(coeffs)


def align_polynomials(all_coeffs: list[Vector]) -> list[Vector]:
    """
    Дополнить незначащями нулями векторы коэффицентов до одинаковой размерности.
    """
    if not all_coeffs:
        raise ValueError("Ввод не может быть пустым. Введите хотя бы один коэффициент.")

    # Находим максимальную степень
    max_len = max(len(c) for c in all_coeffs)

    # Дополняем каждый список нулями в конец
    aligned = []
    for coeffs in all_coeffs:
        padded = coeffs + [Fraction(0)] * (max_len - len(coeffs))
        aligned.append(padded)

    return aligned
