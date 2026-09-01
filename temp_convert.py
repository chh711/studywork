import math

# 各温标绝对零度值（物理下限）
ABSOLUTE_ZERO_C: float = -273.15
ABSOLUTE_ZERO_F: float = -459.67
ABSOLUTE_ZERO_K: float = 0.0


def celsius_to_fahrenheit(celsius: float) -> float:
    """将摄氏温度转换为华氏温度。"""
    return celsius * 9.0 / 5.0 + 32.0


def celsius_to_kelvin(celsius: float) -> float:
    """将摄氏温度转换为开氏温度。"""
    return celsius + 273.15


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """将华氏温度转换为摄氏温度。"""
    return (fahrenheit - 32.0) * 5.0 / 9.0


def fahrenheit_to_kelvin(fahrenheit: float) -> float:
    """将华氏温度转换为开氏温度。"""
    return (fahrenheit - 32.0) * 5.0 / 9.0 + 273.15


def kelvin_to_celsius(kelvin: float) -> float:
    """将开氏温度转换为摄氏温度。"""
    return kelvin - 273.15


def kelvin_to_fahrenheit(kelvin: float) -> float:
    """将开氏温度转换为华氏温度。"""
    return (kelvin - 273.15) * 9.0 / 5.0 + 32.0


class TemperatureConversionError(Exception):
    """温度转换过程中发生的自定义异常。"""
    pass


def get_temperature(prompt: str, *, min_value: float | None = None) -> float:
    """获取有效的温度值，包含完整的异常处理。

    Args:
        prompt: 提示用户输入的字符串。
        min_value: 温度下限（如绝对零度），None 表示不检查下限。

    Returns:
        用户输入的有效温度值（float）。

    Raises:
        TemperatureConversionError: 当用户中断输入或遇到 EOF 时抛出。
    """
    while True:
        try:
            raw = input(prompt)
            value = float(raw)
            # 拒绝 NaN 和 Infinity
            if math.isnan(value) or math.isinf(value):
                print("错误：请输入有效的有限数字，不支持 NaN 或 Infinity。")
                continue
            if min_value is not None and value < min_value:
                print(f"错误：温度不能小于 {min_value}（绝对零度），请重新输入。")
                continue
            return value
        except ValueError:
            print("错误：请输入有效的数字。")
        except EOFError:
            raise TemperatureConversionError("输入流意外结束。")
        except KeyboardInterrupt:
            raise TemperatureConversionError("用户取消了输入。")


def main() -> None:
    """温度单位换算器主入口，提供交互式菜单驱动界面。"""

    print("===== 温度单位换算器 =====")
    print("支持：摄氏 (°C)、华氏 (°F)、开氏 (K)")
    print("输入对应的数字选择转换方向：")
    print("1. 摄氏 → 华氏")
    print("2. 摄氏 → 开氏")
    print("3. 华氏 → 摄氏")
    print("4. 华氏 → 开氏")
    print("5. 开氏 → 摄氏")
    print("6. 开氏 → 华氏")
    print("0. 退出")

    while True:
        try:
            choice = input("\n请选择 (0-6): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        if choice == "0":
            print("再见！")
            break

        if choice not in {"1", "2", "3", "4", "5", "6"}:
            print("无效选项，请重新输入。")
            continue

        try:
            if choice == "1":
                temp = get_temperature("请输入摄氏温度: ", min_value=ABSOLUTE_ZERO_C)
                result = celsius_to_fahrenheit(temp)
                print(f"{temp} °C = {result:.2f} °F")
            elif choice == "2":
                temp = get_temperature("请输入摄氏温度: ", min_value=ABSOLUTE_ZERO_C)
                result = celsius_to_kelvin(temp)
                print(f"{temp} °C = {result:.2f} K")
            elif choice == "3":
                temp = get_temperature("请输入华氏温度: ", min_value=ABSOLUTE_ZERO_F)
                result = fahrenheit_to_celsius(temp)
                print(f"{temp} °F = {result:.2f} °C")
            elif choice == "4":
                temp = get_temperature("请输入华氏温度: ", min_value=ABSOLUTE_ZERO_F)
                result = fahrenheit_to_kelvin(temp)
                print(f"{temp} °F = {result:.2f} K")
            elif choice == "5":
                temp = get_temperature("请输入开氏温度 (Kelvin): ", min_value=ABSOLUTE_ZERO_K)
                result = kelvin_to_celsius(temp)
                print(f"{temp} K = {result:.2f} °C")
            elif choice == "6":
                temp = get_temperature("请输入开氏温度 (Kelvin): ", min_value=ABSOLUTE_ZERO_K)
                result = kelvin_to_fahrenheit(temp)
                print(f"{temp} K = {result:.2f} °F")
        except TemperatureConversionError as e:
            print(f"\n{e} 再见！")
            break


if __name__ == "__main__":
    try:
        main()
    except TemperatureConversionError as e:
        # 防御性兜底：main() 内部已捕获该异常，此处正常情况下不可达，
        # 保留作为安全网以防未来重构导致异常逃逸。
        print(f"\n{e} 再见！")
    except (EOFError, KeyboardInterrupt):
        print("\n程序被中断，再见！")
