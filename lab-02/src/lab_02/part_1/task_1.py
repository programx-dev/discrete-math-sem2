import sys

from models import FUNCTION_REGISTRY
from solver import run_solver


def get_input(prompt: str, default: str) -> str:
    """Вспомогательная функция для ввода со значением по умолчанию."""
    user_input = input(f"{prompt} [{default}]: ").strip()
    return user_input if user_input else default


def main():
    print("\n" + "=" * 50)
    print("      МЕТОД НЬЮТОНА (Решение уравнений)")
    print("=" * 50)

    print("\nДоступные уравнения:")
    for i, f_cls in enumerate(FUNCTION_REGISTRY, 1):
        print(f"  {i}. {f_cls.view}")

    while True:
        try:
            choice_str = get_input("\nВыберите номер уравнения", "1")
            choice = int(choice_str) - 1
            selected_cls = FUNCTION_REGISTRY[choice]
            break
        except (ValueError, IndexError):
            print("  Ошибка: введите число от 1 до", len(FUNCTION_REGISTRY))

    try:
        if hasattr(selected_cls, "from_input"):
            f_instance = selected_cls.from_input()
        else:
            f_instance = selected_cls()
    except ValueError as e:
        print(f"  Ошибка параметров функции: {e}")
        sys.exit(1)

    while True:
        try:
            n_str = get_input("Точность n (для eps = 10^-n)", "6")
            n_digits = int(n_str)
            epsilon = 10**-n_digits
            break
        except ValueError:
            print("  Ошибка: введите целое число (напр. 6 для точности 0.000001)")

    print(f"\nРекомендованные x0: {f_instance.default_x0}")
    mode = get_input("Использовать их? (Y/n)", "y").lower()

    if mode == "y":
        x0 = f_instance.default_x0
    else:
        while True:
            try:
                raw_x0 = input("  Введите x0 через пробел: ").strip()
                if not raw_x0:
                    print("  Список не может быть пустым.")
                    continue
                x0 = [float(x) for x in raw_x0.split()]
                break
            except ValueError:
                print("  Ошибка: введите числа через пробел (напр: -1.0 1.5)")

    try:
        run_solver(f_instance, x0, epsilon)
    except KeyboardInterrupt:
        print("\n\nРешение прервано пользователем.")
    except Exception as e:
        print(f"\nКритическая ошибка при расчете: {e}")

    print("\n" + "=" * 50)
    print("Работа программы завершена.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрограмма закрыта.")
        sys.exit(0)
