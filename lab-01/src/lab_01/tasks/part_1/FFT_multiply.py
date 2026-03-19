import cmath
import math
from collections.abc import Sequence


def FFT(n: int, omega: complex, f: Sequence[complex]) -> list[complex]:
    if n == 1:
        return [f[0]]

    r0 = [f[j] + f[j + n // 2] for j in range(n // 2)]
    r1 = [0j] * (n // 2)

    curr_omega = 1.0 + 0j
    for j in range(n // 2):
        r1[j] = (f[j] - f[j + n // 2]) * curr_omega
        curr_omega *= omega

    omega_sq = omega**2

    A = FFT(n // 2, omega_sq, r0)
    B = FFT(n // 2, omega_sq, r1)

    # Четные позиции из A, нечетные из B
    res = [0j] * n
    for j in range(n // 2):
        res[2 * j] = A[j]
        res[2 * j + 1] = B[j]

    return res


def multiply(f: list[float], g: list[float]) -> list[float]:
    target_deg = (len(f) - 1) + (len(g) - 1)

    n = 1
    while n <= target_deg:
        n *= 2

    # Дополняем нулями до длины n
    f_padded = f + [0.0] * (n - len(f))
    g_padded = g + [0.0] * (n - len(g))

    # Прямое FFT
    omega = cmath.exp(complex(0, 2 * math.pi / n))
    dft_f = FFT(n, omega, f_padded)
    dft_g = FFT(n, omega, g_padded)

    # Покомпонентное умножение
    component_prod = [x * y for x, y in zip(dft_f, dft_g)]

    # Обратное FFT
    omega_inv = 1 / omega
    inv_fft_res = FFT(n, omega_inv, component_prod)
    prod_f_g = [x.real / n for x in inv_fft_res]

    # Обрезаем лишние нули в конце
    while len(prod_f_g) > target_deg + 1 and abs(prod_f_g[-1]) < 1e-9:
        prod_f_g.pop()

    return prod_f_g


def main():
    f = [-1., 1]
    g = [1., 1, 1]

    res = multiply(f, g)

    # Округлим для красоты
    print([round(x, 2) for x in res])


if __name__ == "__main__":
    main()
