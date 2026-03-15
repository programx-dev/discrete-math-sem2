from collections.abc import Iterable, Sequence

from models import TypeF


def method_newton(
    f_obj: TypeF, x0: float, epsilon: float, max_depth: int = 100
) -> Iterable[float]:
    DERIVATIVE_EPS = 1e-12
    SHIFT = 1e-4
    current_x = x0

    for _ in range(max_depth):
        f_val = f_obj.f(current_x)
        f_der = f_obj.f_derivative(current_x)

        if abs(f_der) < DERIVATIVE_EPS:
            current_x += SHIFT
            f_der = f_obj.f_derivative(current_x)
            if abs(f_der) < DERIVATIVE_EPS:
                raise RuntimeError("Производная в этой точке близка к нулю.")

        next_x = current_x - f_val / f_der
        yield next_x

        if abs(next_x - current_x) < epsilon:
            return
        current_x = next_x


def run_solver(f_obj: TypeF, x0_list: Sequence[float], epsilon: float):
    print(f"\nРезультаты для функции: {f_obj.view}")
    print("-" * 40)
    for x_start in x0_list:
        print(f"Начальное приближение x0 = {x_start}:")
        try:
            for i, x_curr in enumerate(method_newton(f_obj, x_start, epsilon), 1):
                print(f"  [{i}] x = {x_curr:.10f}")
        except Exception as e:
            print(f"  Ошибка: {e}")
