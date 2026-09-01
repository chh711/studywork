"""
类型标注（Type Hints）完整演示
================================
Python 类型标注不会在运行时检查，但它配合 mypy / pyright / IDE
能在你写代码时就暴露 bug —— 不需要等到跑起来才炸。

本文件覆盖：
  1. 基本类型注解：int, str, float, bool, list, dict, tuple
  2. Optional[T] = T | None
  3. 函数签名标注：参数类型、返回值类型
  4. 用 mypy 静态检查，提前暴露 bug
"""

from typing import Optional, Union, Any

# ============================================================
# 一、基本类型注解
# ============================================================

# 变量标注（通常 IDE 能推断，但复杂场景显式标注更安全）
name: str = "Alice"
age: int = 30
height: float = 1.75
is_active: bool = True

# 容器类型
scores: list[int] = [85, 92, 78]           # list[T]  Python 3.9+
config: dict[str, int] = {"port": 8080}     # dict[K, V]
point: tuple[float, float] = (3.5, 4.2)


# ============================================================
# 二、函数签名标注
# ============================================================

def calculate_grade(scores: list[int]) -> float:
    """
    参数标注 + 返回值标注
    scores: list[int]  → 接收整数列表
    -> float           → 返回浮点数
    """
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def find_user(users: dict[str, int], name: str) -> int | None:
    """
    返回值 int | None：可能找不到用户，返回 None
    这是 Optional[int] 的现代写法（Python 3.10+）
    """
    return users.get(name)


# ============================================================
# 三、Optional[T] —— "这个值可能不存在"
# ============================================================

# 旧写法
def get_port_old(config: dict[str, str]) -> Optional[int]:
    ...  # Optional[int] = Union[int, None]

# 新写法（Python 3.10+，推荐）
def get_port(config: dict[str, str]) -> int | None:
    """
    从配置中提取端口号，不存在则返回 None
    int | None 比 Optional[int] 更直观
    """
    if "port" not in config:
        return None
    return int(config["port"])


# ============================================================
# 四、类型标注如何提前暴露 bug
# ============================================================

# --- Bug 示例 1：传错类型 ---
def send_money(amount: float) -> str:
    """转账金额必须是数值"""
    return f"转账 {amount:.2f} 元"

def bug_demo_wrong_type():
    # mypy 会报：error: Argument 1 to "send_money" has incompatible type "str"
    result = send_money("一百块")   # 传了字符串，mypy 立刻发现
    print(result)


# --- Bug 示例 2：Optional 忘判空 ---
def greet(user_name: str | None) -> str:
    """
    参数是 Optional，但代码直接调用了 .upper()
    mypy 会报：Item "None" of "str | None" has no attribute "upper"
    """
    # 错误写法：没判空就调用方法
    # return f"Hello, {user_name.upper()}"   # mypy 报错！

    # 正确写法：先判空
    if user_name is None:
        return "Hello, Anonymous"
    return f"Hello, {user_name.upper()}"


# --- Bug 示例 3：返回值可能为 None，调用方没处理 ---
def find_student(students: dict[int, str], sid: int) -> str | None:
    return students.get(sid)

def bug_demo_unchecked_none():
    students: dict[int, str] = {1: "Alice", 2: "Bob"}
    name = find_student(students, 99)   # -> None
    # mypy 报：error: Item "None" of "str | None" has no attribute "upper"
    print(name.upper())          # None.upper() 会炸！


# --- Bug 示例 4：list 元素类型不一致 ---
def sum_all(numbers: list[int]) -> int:
    return sum(numbers)

def bug_demo_list_mismatch():
    # mypy 报：error: List item 3 has incompatible type "str"
    result = sum_all([1, 2, "3", 4])   # 混入了字符串
    print(result)


# ============================================================
# 五、实战演示
# ============================================================

def demo():
    print("=" * 60)
    print("  类型标注演示")
    print("=" * 60)

    # 正常使用
    print("\n>> 1. 正常类型使用")
    avg = calculate_grade([88, 92, 76, 95])
    print(f"   平均分: {avg}  (type: {type(avg).__name__})")

    users = {"Alice": 30, "Bob": 25}
    found = find_user(users, "Alice")
    not_found = find_user(users, "Charlie")
    print(f"   找到 Alice: {found}  (type: {type(found).__name__})")
    print(f"   未找到 Charlie: {not_found}  (type: {type(not_found).__name__})")

    # Optional 使用
    print("\n>> 2. Optional / int | None")
    cfg1 = {"host": "localhost", "port": "8080"}
    cfg2 = {"host": "localhost"}
    print(f"   port 存在: {get_port(cfg1)}")
    print(f"   port 缺失: {get_port(cfg2)}")

    # Optional 判空
    print("\n>> 3. Optional 判空保护")
    print(f"   {greet('Alice')}")
    print(f"   {greet(None)}")

    # Bug 演示（运行时就会炸，但 mypy 可以提前发现）
    print("\n>> 4. 运行时暴露的 bug（mypy 提前就能发现）")

    print("  [Bug 1] send_money('一百块') —— 传了 str 给 float 参数:")
    try:
        bug_demo_wrong_type()
    except ValueError as e:
        print(f"    运行时炸了: {e}")

    print("  [Bug 2] 返回值 Optional 忘判空:")
    try:
        bug_demo_unchecked_none()
    except AttributeError as e:
        print(f"    运行时炸了: {e}")

    print("  [Bug 3] list[int] 混入 str:")
    try:
        bug_demo_list_mismatch()
    except TypeError as e:
        print(f"    运行时炸了: {e}")

    print("\n" + "=" * 60)
    print("  mypy 可以在写代码时就发现以上全部 bug，无需运行")
    print("  运行: mypy eafp_demo.py")
    print("=" * 60)


if __name__ == "__main__":
    demo()
