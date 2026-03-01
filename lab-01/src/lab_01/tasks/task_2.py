# task_2.py

import sys
from fractions import Fraction
from lab_01.math_engine.matrix import Matrix, MatrixError, Vector
from lab_01.math_engine.solver import Solver, Solution
from lab_01.polynomials.model import Polynomial
from lab_01.polynomials.parser import parse_coeff_string


def format_binomial_decomposition(solution: Solution, a: Fraction) -> str:
    """
    Форматирует ответ в виде суммы A_k * (x - a)^k.
    """
    if not solution or not solution.particular:
        return "Решений нет."

    parts = []
    for k, coeff in enumerate(solution.particular):
        if coeff == 0:
            continue

        # Работа со знаком
        sign = " + " if coeff > 0 else " - "
        if not parts:
            sign = "" if coeff > 0 else "-"

        # Форматирование коэффициента A_k
        abs_c = abs(coeff)
        c_str = f"({abs_c})" if abs_c.denominator != 1 else str(abs_c)

        # Форматирование скобки (x - a)^k
        if k == 0:
            term = c_str
        else:
            # Красиво оформляем (x - a)
            if a == 0:
                base = "x"
            else:
                op = "-" if a > 0 else "+"
                base = f"(x {op} {abs(a)})"

            power = f"^{k}" if k > 1 else ""

            # Если коэффициент 1, не пишем его перед скобкой
            term = f"{base}{power}" if abs_c == 1 else f"{c_str}*{base}{power}"

        parts.append(f"{sign}{term}")

    return "f(x) = " + "".join(parts) if parts else "f(x) = 0"


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


def create_matrix(f_vector: Vector, a: Fraction) -> Matrix:
    """
    Создает расширенную матрицу системы для разложения по (x-a)^k.
    """

    max_deg = len(f_vector) - 1
    cols = [get_col(k, a, max_deg) for k in range(max_deg + 1)]

    return Matrix.from_columns(cols).augment(f_vector)


def main():
    print("=== Разложение многочлена по степеням (x - a) ===")
    try:
        # Ввод
        f_vector = parse_coeff_string(input("Коэффициенты f(x) (x^0 x^1 ...): "))
        a = Fraction(input("Введите число a: "))

        # Решение
        print(f"\nВаш многочлен: {Polynomial(f_vector)}")
        matrix_system = create_matrix(f_vector, a)

        print("\nМатрица системы:")
        print(matrix_system)

        solution = Solver.solve(matrix_system)

        # Вывод
        print("\n--- Итоговое разложение ---")
        print(format_binomial_decomposition(solution, a))
        print("===========================================\n")

    except (MatrixError, ValueError, KeyboardInterrupt) as e:
        print(f"\nКритическая ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
