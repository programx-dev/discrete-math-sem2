# task_8_1.py


def method_7_mult(a0: float, a1: float, b0: float, b1: float) -> complex:
    b0_sq = b0 * b0
    b1_sq = b1 * b1
    denom = b0_sq + b1_sq

    a0b0 = a0 * b0
    a1b1 = a1 * b1

    prod = (a0 + a1) * (b0 - b1)
    num_im = prod - a0b0 + a1b1
    num_re = a0b0 + a1b1

    re = num_re / denom
    im = num_im / denom

    return complex(re, im)


def method_6_mult(a0: float, a1: float, b0: float, b1: float) -> complex:
    r = b0 / b1

    a0r = a0 * r
    a1r = a1 * r

    denom = b0 * r + b1

    re = (a0r + a1) / denom
    im = (a1r - a0) / denom

    return complex(re, im)


def main():
    A = complex(input("Введите комплексное число z1 (например, 2+3j): "))
    B = complex(input("Введите комплексное число z2 (например, 2+3j): "))

    a0, a1 = A.real, A.imag
    b0, b1 = B.real, B.imag

    res1 = method_7_mult(a0, a1, b0, b1)
    res2 = method_6_mult(a0, a1, b0, b1)

    print(f"z1/z2 = {res1}")
    print(f"z1/z2 = {res2}")


if __name__ == "__main__":
    main()
