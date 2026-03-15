import math
from dataclasses import dataclass, field
from typing import Protocol


class TypeF(Protocol):
    view: str
    default_x0: list[float]

    def f(self, x: float) -> float: ...
    def f_derivative(self, x: float) -> float: ...


@dataclass
class F1:
    view: str = "sin(x) - 2x^2 + 0.5"
    default_x0: list[float] = field(default_factory=lambda: [-1.0, 1.0])

    def f(self, x: float) -> float:
        return math.sin(x) - 2 * x**2 + 0.5

    def f_derivative(self, x: float) -> float:
        return math.cos(x) - 4 * x


@dataclass
class F2:
    view: str = "x^n = a"
    default_x0: list[float] = field(default_factory=lambda: [-2.0, 2.0])
    a: float = 2.0
    n: int = 2

    def f(self, x: float) -> float:
        return x**self.n - self.a

    def f_derivative(self, x: float) -> float:
        return self.n * (x ** (self.n - 1))

    @classmethod
    def from_input(cls):
        print("\n--- Настройка функции x^n = a ---")
        a = float(input("  Введите параметр a (a > 0): "))
        n = int(input("  Введите степень n: "))
        return cls(a=a, n=n)


@dataclass
class F3:
    view: str = "sqrt(1 - x^2) - e^x + 0.1"
    default_x0: list[float] = field(default_factory=lambda: [-0.9, 0.5])

    def f(self, x: float) -> float:
        return math.sqrt(1 - x**2) - math.exp(x) + 0.1

    def f_derivative(self, x: float) -> float:
        return -x / math.sqrt(1 - x**2) - math.exp(x)


@dataclass
class F4:
    view: str = "x^6 = 5x^3 + 2"
    default_x0: list[float] = field(default_factory=lambda: [-5.0, 5.0])

    def f(self, x: float) -> float:
        return x**6 - 5 * x**3 - 2

    def f_derivative(self, x: float) -> float:
        return 6 * x**5 - 15 * x**2


@dataclass
class F5:
    view: str = "log2(x) = 1/(1+x^2)"
    default_x0: list[float] = field(default_factory=lambda: [0.1, 2.0])

    def f(self, x: float) -> float:
        return math.log2(x) - 1 / (1 + x**2)

    def f_derivative(self, x: float) -> float:
        return 1 / (x * math.log(2)) + (2 * x) / ((1 + x**2) ** 2)


@dataclass
class F6:
    view: str = "sin(x/2) = 1"
    default_x0: list[float] = field(default_factory=lambda: [-5.0, 1.0, 15.0])

    def f(self, x: float) -> float:
        return math.sin(x / 2) - 1

    def f_derivative(self, x: float) -> float:
        return math.cos(x / 2) / 2


@dataclass
class F7:
    view: str = "ln(x) = 1"
    default_x0: list[float] = field(default_factory=lambda: [0.1, 1.0, 5.0])

    def f(self, x: float) -> float:
        return math.log(x) - 1

    def f_derivative(self, x: float) -> float:
        return 1 / x


FUNCTION_REGISTRY = [F1, F2, F3, F4, F5, F6, F7]
