from math import ceil, log2
from typing import Sequence


def is_close(x: float) -> bool:
    """Проверка на близость к нулю с учетом погрешности float."""
    return abs(x) < 1e-12


def format_series(coefs: list[float], n: int, precision: int = 4) -> str:
    """Красивый вывод первых n членов ряда в виде a0 + a1*x + a2*x^2..."""
    parts = []
    for i, c in enumerate(coefs[:n]):
        if is_close(c):
            continue
        c_round = round(c, precision)
        if i == 0:
            parts.append(f"{c_round}")
        elif i == 1:
            parts.append(f"{c_round:+}*x")
        else:
            parts.append(f"{c_round:+}*x^{i}")
    return " ".join(parts) if parts else "0"


def is_unit(f_product: list[float]) -> bool:
    """Проверяет, является ли весь список коэффициентов единичным рядом (1, 0, 0...)."""
    if not f_product:
        return False
    if not is_close(f_product[0] - 1.0):
        return False
    return all(is_close(x) for x in f_product[1:])


def get_coef_multiple(f: list[float], g: list[float], limit: int) -> list[float]:
    """Произведение двух многочленов до степени limit-1."""
    deg_f = len(f) - 1
    deg_g = len(g) - 1
    coefs = [0.0] * limit

    for k in range(limit):
        for j in range(max(0, k - deg_g), min(k, deg_f) + 1):
            coefs[k] += f[j] * g[k - j]
    return coefs


def minus_coeff(f: list[float], g: list[float]) -> list[float]:
    """Разность двух многочленов с поддержкой разной длины."""
    size = max(len(f), len(g))
    res = [0.0] * size
    for i in range(size):
        val_f = f[i] if i < len(f) else 0.0
        val_g = g[i] if i < len(g) else 0.0
        res[i] = val_f - val_g
    return res


def newton_inverse(f: Sequence[float], l: int) -> list[float]:
    """Находит первые l коэффициентов обратного ряда f^-1 методом Ньютона."""
    if not f or is_close(f[0]):
        raise ValueError("Ряд не обратим: a0 должен быть отличным от нуля.")

    g = [1.0 / f[0]]
    k = ceil(log2(l))

    for i in range(1, k + 1):
        limit = 2**i

        # Формула Ньютона: g = 2g - f * g^2
        g_sq = get_coef_multiple(g, g, limit)
        f_g_sq = get_coef_multiple(g_sq, list(f), limit)
        two_g = [x * 2.0 for x in g]

        g = minus_coeff(two_g, f_g_sq)

    return g[:l]


def run_test_case(name: str, f: list[float], n: int):
    print(f"\n{'=' * 20} {name} {'=' * 20}")
    try:
        f_inv = newton_inverse(f, n)
        product = get_coef_multiple(f, f_inv, limit=n)

        print(f"Исходный ряд f: {format_series(f, len(f))}")
        print(f"Обратный ряд f^-1: {format_series(f_inv, n)}")

        print(f"\nПроверка (f * f^-1 mod x^{n})")
        print(f"Результат: {format_series(product, len(product))}")
        print(f"f * f^-1 == 1: {is_unit(product)}")

    except ValueError as e:
        print(f"Ошибка: {e}")


def main():
    # Пример (1): Ряд Тейлора для экспоненты e^x (M=10)
    # f = 1 + x + x^2/2! + x^3/3! ...
    M = 10
    n = 10
    f_exp = [1.0]
    fact = 1.0
    for i in range(1, M + 1):
        fact *= i
        f_exp.append(1.0 / fact)

    run_test_case(f"Пример (1): Экспонента (M={M})", f_exp, n)

    # Пример (2): Многочлен f = x^2 - x - 1
    f_poly = [-1.0, -1.0, 1.0]
    run_test_case("Пример (2): f = x^2 - x - 1", f_poly, 10)


if __name__ == "__main__":
    main()
