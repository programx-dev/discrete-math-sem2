# task_3.py

import sys
from fractions import Fraction
from lab_01.math_engine.matrix import Matrix, MatrixError
from lab_01.polynomials.parser import parse_coeff_string
from lab_01.tasks.part_1.task_2 import format_binomial_decomposition
from lab_01.polynomials.binomial import get_col


def create_transition_matrix(num_vars: int, h: Fraction) -> Matrix:
    """
    Создает матрицу перехода S.
    """
    cols = [get_col(j, -h, num_vars - 1) for j in range(num_vars)]

    return Matrix.from_columns(cols)


def main():
    print("=== Переход между базисами (x-a) -> (x-B) ===")
    try:
        f_coeffs = parse_coeff_string(
            input(
                "Введите коэффициенты f_j при степенях (x - a)^j (через пробел, от j=0): "
            )
        )

        a = Fraction(input("Введите число a: "))
        B = Fraction(input("Введите число B: "))

        h = B - a
        num_vars = len(f_coeffs)

        S = create_transition_matrix(num_vars, h)

        print("\nМатрица перехода S (в столбцах разложения ( (x - B) + h )^j ):")
        print(S)

        result_matrix = S @ f_coeffs
        b_coeffs = result_matrix.get_column(0)

        # Используем Solution как контейнер, чтобы переиспользовать format_binomial_decomposition
        from lab_01.math_engine.solver import Solution

        mock_solution = Solution(particular=b_coeffs)

        print("\n--- Итоговое представление ---")
        print(format_binomial_decomposition(mock_solution, B))
        print("========================================================\n")

    except (MatrixError, ValueError, KeyboardInterrupt) as e:
        print(f"\nКритическая ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
