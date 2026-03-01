# matrix.py

from fractions import Fraction
from typing import Sequence, Union, cast


type Vector = list[Fraction]


class MatrixError(Exception):
    pass


class MatrixValidator:
    """
    Валидация матрицы.
    """

    @staticmethod
    def validate(data: list[Vector]):
        """
        Валидация матрицы.
        """
        if not data:
            raise MatrixError("Матрица пустая.")

        if not data[0]:
            raise MatrixError("Неверная размерность.")

        cols = len(data[0])
        if not all(len(row) == cols for row in data):
            raise MatrixError("Неверная размерность.")


class Matrix:
    """
    Матрица из Fraction. Индексация строк и столбцов ведется с 0.
    """

    def __init__(self, data: list[Vector]):
        """
        Создать объект матрицы на основе строк Fraction.
        """

        MatrixValidator.validate(data)

        self.rows = len(data)
        self.cols = len(data[0])

        self._data = [list(row) for row in data]

    def __getitem__(self, key: tuple[int, int]) -> Fraction:
        """
        Получить значение по индексу.
        """
        r, c = key

        self._validate_indices(r, c)

        return self._data[r][c]

    def __setitem__(self, key: tuple[int, int], value: Fraction):
        """
        Установить значение по индексу.
        """
        r, c = key

        self._validate_indices(r, c)

        self._data[r][c] = value

    def cross_row(self, row: int) -> "Matrix":
        """
        Вычеркнуть строку. Создается новая матрица.
        """
        self._validate_indices(row)

        new_data = [vector for r, vector in enumerate(self._data) if r != row]
        return Matrix(new_data)

    def cross_col(self, col: int) -> "Matrix":
        """
        Вычеркнуть столбец. Создается новая матрица.
        """
        self._validate_indices(col=col)

        new_data = [
            [item for c, item in enumerate(row) if c != col] for row in self._data
        ]
        return Matrix(new_data)

    @staticmethod
    def data_to_fraction(data: Sequence[Sequence[Union[int, float]]]) -> list[Vector]:
        """
        Конвертировать матрицу из чисел в матрицу из Fraction.
        """
        return [[Fraction(i) for i in row] for row in data]

    def _validate_indices(self, row: int | None = None, col: int | None = None):
        """
        Проверить индексы на нахождение в диапазоне.
        """
        if row is not None and not (0 <= row < self.rows):
            raise MatrixError("Указана несуществующая строка.")

        if col is not None and not (0 <= col < self.cols):
            raise MatrixError("Указан несуществущий столбец.")

    def add_row_multiple(self, dest: int, src: int, coeff: Fraction = Fraction(1)):
        """
        Прибавить к строке dest строку src, умноженную на coeff.
        """
        self._validate_indices(dest)
        self._validate_indices(src)

        if src == dest:
            raise MatrixError("Указана одна и та же строка.")

        for c in range(self.cols):
            self._data[dest][c] += self._data[src][c] * coeff

    def multiply_row(self, dest: int, coeff: Fraction):
        """
        Домножить строку на число.
        """
        self._validate_indices(dest)

        for c in range(self.cols):
            self._data[dest][c] *= coeff

    def swap_rows(self, dest: int, src: int):
        """
        Переставить строки.
        """
        self._validate_indices(dest)
        self._validate_indices(src)

        self._data[dest], self._data[src] = self._data[src], self._data[dest]

    def swap_cols(self, dest: int, src: int):
        """
        Переставить столбцы.
        """
        self._validate_indices(dest)
        self._validate_indices(src)

        for r in range(self.rows):
            self._data[r][dest], self._data[r][src] = (
                self._data[r][src],
                self._data[r][dest],
            )

    def get_column(self, column: int) -> Vector:
        """
        Получить матрицу-столбец.
        """
        self._validate_indices(col=column)

        return [self._data[r][column] for r in range(self.rows)]

    def get_row(self, row: int) -> Vector:
        """
        Получить матрицу-строку.
        """
        self._validate_indices(row)

        return list(self._data[row])

    def copy(self) -> "Matrix":
        """
        Скопировать матрицу.
        """
        return Matrix(self._data)

    @property
    def data(self) -> list[Vector]:
        """
        Поле data.
        """
        return [list(row) for row in self._data]

    @staticmethod
    def _transpose(data: list[Vector]) -> list[Vector]:
        """
        Транспонировать матрицу значений.
        """
        cols = len(data)
        rows = len(data[0])

        return [[data[c][r] for c in range(cols)] for r in range(rows)]

    @classmethod
    def from_columns(cls, data: list[Vector]) -> "Matrix":
        """
        Создать матрицу из вектора столбцов.
        """
        MatrixValidator.validate(data)

        return cls(data=cls._transpose(data))

    @classmethod
    def empty(cls, rows: int, cols: int) -> "Matrix":
        """
        Создать пустую матрицу.
        """
        data = [[Fraction(0)] * cols for _ in range(rows)]

        return cls(data=data)

    def __str__(self) -> str:
        rows = [[str(item) for item in row] for row in self._data]

        col_widths = [
            max(len(rows[r][c]) for r in range(self.rows)) for c in range(self.cols)
        ]

        lines = []
        for row in rows:
            line = "  ".join(f"{item:>{col_widths[c]}}" for c, item in enumerate(row))
            lines.append(line)

        return "\n".join(lines)

    def augment(self, other: Union["Matrix", list[Vector], Vector]) -> "Matrix":
        """
        Расширить матрицу.
        Позволяет конкатенировать с другой матрицей, матрицей значений или мектором-строкой.
        """
        other_rows: list[Vector]

        if isinstance(other, Matrix):
            other_rows = other.data
        elif isinstance(other, list):
            if not other:
                raise MatrixError("Пустая коллекция.")

            if isinstance(other[0], Fraction):
                flat_list = cast(Vector, other)
                other_rows = [[item] for item in flat_list]
            elif isinstance(other[0], list):
                other_rows = cast(list[Vector], other)
            else:
                raise MatrixError("Неподдерживаемое содержимое списка.")

            MatrixValidator.validate(other_rows)
        else:
            raise MatrixError("Неподдерживаемый тип аргумента.")

        if len(other_rows) != self.rows:
            raise MatrixError("Неверная размерность.")

        data = [self._data[r] + other_rows[r] for r in range(self.rows)]

        return Matrix(data=data)
