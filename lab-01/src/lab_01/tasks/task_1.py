# task_1.py

import sys
from lab_01.math_engine.matrix import Matrix, MatrixError, Vector
from lab_01.math_engine.solver import Solver, Solution
from lab_01.polynomials.model import Polynomial
from lab_01.polynomials.parser import parse_coeff_string, align_polynomials


def format_vector(v: Vector) -> str:
    """
    Строковое представление ЛК.
    """
    parts = []
    for i, coeff in enumerate(v):
        if coeff == 0:
            continue

        # Логика знаков
        sign = " + " if coeff > 0 else " - "
        if not parts and coeff > 0:
            sign = ""
        elif not parts and coeff < 0:
            sign = "-"

        abs_c = abs(coeff)
        c_str = f"({abs_c})" if abs_c.denominator != 1 else str(abs_c)

        # Не пишем коэффицент 1
        term = f"g_{i + 1}(x)" if abs_c == 1 else f"{c_str}*g_{i + 1}(x)"
        parts.append(f"{sign}{term}")

    return "".join(parts) if parts else "0"


def format_final_answer(solution: Solution) -> str:
    """
    Форматирует решение в виде линейной комбинации многочленов g_i.
    """
    if not solution.particular:
        return "Вектор f не принадлежит линейной оболочке векторов g_i."

    # Частное решение
    particular_str = format_vector(solution.particular)
    res = f"f(x) = {particular_str}"

    # ФСР
    if solution.fsr:
        for i, fsr_vec in enumerate(solution.fsr):
            fsr_str = format_vector(fsr_vec)
            res += f" + C{i + 1}*({fsr_str})"

    return res


def cli_input() -> tuple[Vector, list[Vector]]:
    """
    Сбор данных от пользователя через терминал.
    """
    print("\n--- Ввод данных ---")
    print("Введите коэффициенты через пробел, начиная с x^0 (например: 1 0.5 -1/3)")

    try:
        f_raw = parse_coeff_string(input("Коэффициенты f(x): "))

        k_input = input("Количество порождающих многочленов g_i: ")
        k = int(k_input)

        g_raw_list = []
        for i in range(k):
            s = input(f"Коэффициенты g_{i + 1}(x): ")
            g_raw_list.append(parse_coeff_string(s))

        # Выравнивание длин списков
        all_aligned = align_polynomials([f_raw] + g_raw_list)
        f_vector, *g_vectors = all_aligned

        return f_vector, g_vectors

    except ValueError as e:
        raise MatrixError(f"Ошибка ввода: {e}")


def main():
    print("=== Проверка принадлежности многочлена линейной оболочке ===")

    try:
        f, g = cli_input()
    except (MatrixError, ValueError) as e:
        print(f"\nКритическая ошибка: {e}")
        sys.exit(1)

    # Интерпретация ввода
    print("\n--- Ваши многочлены ---")
    print(f"f(x) = {Polynomial(f)}")
    for i, vec in enumerate(g):
        print(f"g_{i + 1}(x) = {Polynomial(vec)}")

    # Формируем матрицу системы
    matrix_system = Matrix.from_columns(g).augment(f)

    print("\n--- Расширенная матрица системы [G | f] ---")
    print(matrix_system)

    # Решаем систему
    solution = Solver.solve(matrix_system)

    # Выводим результат
    print("\n--- Результат решения СЛАУ ---")
    print(solution)

    print("\n--- Итоговое представление ---")
    print(format_final_answer(solution))
    print("============================================================\n")


if __name__ == "__main__":
    main()
