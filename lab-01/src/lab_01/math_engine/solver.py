# solver.py

from fractions import Fraction

from lab_01.math_engine.matrix import Matrix, Vector


class Solution:
    """
    Объект решения СЛАУ.
    """

    def __init__(
        self, particular: Vector | None = None, fsr: list[Vector] | None = None
    ) -> None:
        self.particular = list(particular) if particular else None
        self.fsr = [list(v) for v in fsr] if fsr else []
        self.num_vars = len(self.particular) if self.particular else 0

    def get_full_solution(self, coeffs: list[Fraction] | None = None) -> Vector:
        """
        Вычисляет конкретное решение при заданных C1, C2...
        """
        if not self.particular:
            raise ValueError("Решений нет.")

        if coeffs is None:
            return list(self.particular)

        if len(coeffs) != len(self.fsr):
            raise ValueError(
                "Количество коэффициентов не совпадает с размерностью ФСР."
            )

        result = list(self.particular)
        for i, c in enumerate(coeffs):
            for j in range(self.num_vars):
                result[j] += self.fsr[i][j] * c

        return result

    def __bool__(self):
        return self.particular is not None

    def __str__(self):
        if self.particular is None:
            return "∅"

        str_particular = ", ".join(str(item) for item in self.particular)
        # Вывод частного решения
        res = f"Частное решение X_p: ({str_particular})\n"

        if not self.fsr:
            return res.strip()

        # Вывод векторов ФСР
        res += "ФСР:\n"
        for i, v in enumerate(self.fsr):
            str_v = ", ".join(str(item) for item in v)
            res += f"  φ[{i + 1}] = ({str_v})\n"

        # Общий вид
        fsr_parts = " + ".join([f"C{i + 1}*φ[{i + 1}]" for i in range(len(self.fsr))])
        res += f"Общее решение: X_p + {fsr_parts}"

        return res


class Solver:
    """
    Решение СЛАУ.
    """

    @staticmethod
    def _find_pivot(matrix: Matrix, start_row: int, column: int) -> int | None:
        """
        Поиск ведущего элемента в заданной column колонеке начиная с start_row строки.
        """
        for row in range(start_row, matrix.rows):
            if matrix[row, column] != 0:
                return row

    @staticmethod
    def gauss_jordan_inplace(src: Matrix) -> tuple[int, int, list[int]]:
        """
        Приведение матрицы к упрощенному виду, возвращает:
        rg(A), rg(A | b), индексы колонок ведущих элементов.
        """
        work_row = 0
        rank_a = 0
        pivot: Fraction
        pivot_cols = []
        rows, cols = src.rows, src.cols

        for work_col in range(cols):
            pivot_row = Solver._find_pivot(src, work_row, work_col)

            if pivot_row is None:
                continue

            if work_col < cols - 1:
                rank_a += 1
                pivot_cols.append(work_col)

            pivot = src[pivot_row, work_col]
            src.swap_rows(pivot_row, work_row)

            # Делим строку на ведущий элемент
            src.multiply_row(work_row, 1 / pivot)

            # Обнуляем элементы над и под ведущим
            for i in range(rows):
                if src[i, work_col] != 0 and i != work_row:
                    src.add_row_multiple(i, work_row, -src[i, work_col])

            work_row += 1

        return rank_a, work_row, pivot_cols

    @staticmethod
    def solve(matrix: Matrix) -> Solution:
        """
        Решение СЛАУ.
        """
        copy_matrix = matrix.copy()

        # Приведение к упрощенному виду
        rg, rg_augment, pivot_cols = Solver.gauss_jordan_inplace(copy_matrix)
        num_vars = matrix.cols - 1

        # Система несовместна
        if rg != rg_augment:
            return Solution(None)

        # Частное решение системы
        particular = [Fraction(0)] * num_vars

        for row, pivot_col in enumerate(pivot_cols):
            particular[pivot_col] = copy_matrix[row, num_vars]

        # Система определенная
        if rg == num_vars:
            return Solution(particular)

        # Поиск ФСР
        fsr = []
        free_cols = [col for col in range(num_vars) if col not in pivot_cols]

        for free_col in free_cols:
            vector = [Fraction(0)] * num_vars

            vector[free_col] = Fraction(1)

            for row, pivot_col in enumerate(pivot_cols):
                vector[pivot_col] = -copy_matrix[row, free_col]

            fsr.append(vector)

        return Solution(particular, fsr)
