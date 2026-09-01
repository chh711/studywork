"""
try / except / finally + raise 自定义异常 + EAFP 风格
======================================================
Python 哲学：EAFP —— Easier to Ask for Forgiveness than Permission
"先做了再说，出问题再处理"，而不是"动手之前先检查一万遍"。

对比：
  LBYL (Look Before You Leap)：if 检查 → 再做
  EAFP (Ask Forgiveness)    ：直接做 → except 兜底

本文件用 5 个递进场景演示这三种概念的配合。
"""

import json
from typing import Any


# ============================================================
# 第 1 步：自定义异常 —— 让错误"会说话"
# ============================================================

class ConfigError(Exception):
    """配置相关所有错误的基类"""
    pass


class MissingKeyError(ConfigError):
    """缺少必需的配置键"""
    def __init__(self, key: str, source: str):
        self.key = key
        self.source = source
        super().__init__(f"缺少必要配置 '{key}'（来源: {source}）")


class InvalidTypeError(ConfigError):
    """配置值类型不对"""
    def __init__(self, key: str, expected: str, actual: str):
        self.key = key
        self.expected = expected
        self.actual = actual
        super().__init__(f"'{key}' 类型错误：期望 {expected}，实际 {actual}")


class OutOfRangeError(ConfigError):
    """配置值超出允许范围"""
    def __init__(self, key: str, value, min_val, max_val):
        self.key = key
        self.value = value
        super().__init__(f"'{key}' = {value} 超出范围 [{min_val}, {max_val}]")


# ============================================================
# 第 2 步：EAFP vs LBYL 对比 —— 同一个任务，两种写法
# ============================================================

def process_config_lbyl(raw: dict) -> dict:
    """
    LBYL 风格：做每一步之前先 if 检查
    问题：检查和执行之间有时间窗口（虽然单线程不明显，但代码又臭又长）
    """
    # 检查字典本身
    if not isinstance(raw, dict):
        raise TypeError(f"需要 dict，实际 {type(raw).__name__}")

    # 检查 host
    if "host" not in raw:
        raise MissingKeyError("host", "config")
    host = raw["host"]
    if not isinstance(host, str):
        raise InvalidTypeError("host", "str", type(host).__name__)

    # 检查 port
    if "port" not in raw:
        raise MissingKeyError("port", "config")
    port = raw["port"]
    if not isinstance(port, int):
        raise InvalidTypeError("port", "int", type(port).__name__)
    if not (1 <= port <= 65535):
        raise OutOfRangeError("port", port, 1, 65535)

    # 检查 timeout
    if "timeout" in raw:
        timeout = raw["timeout"]
        if not isinstance(timeout, (int, float)):
            raise InvalidTypeError("timeout", "int/float", type(timeout).__name__)
        if timeout < 0:
            raise OutOfRangeError("timeout", timeout, 0, "∞")

    return {"host": host, "port": port, "timeout": raw.get("timeout", 30)}


def process_config_eafp(raw: dict) -> dict:
    """
    EAFP 风格：直接取值/转换，出问题再捕获
    代码量减半，逻辑更清晰
    """
    try:
        host = raw["host"]          # 直接取，KeyError 说明缺 key
        port = raw["port"]
        timeout = raw.get("timeout", 30)
    except KeyError as e:
        raise MissingKeyError(e.args[0], "config") from e

    # 类型校验：直接用 int() 转换，失败说明类型不对
    try:
        port = int(port)
    except (ValueError, TypeError) as e:
        raise InvalidTypeError("port", "int", type(port).__name__) from e

    if not (1 <= port <= 65535):
        raise OutOfRangeError("port", port, 1, 65535)

    return {"host": host, "port": port, "timeout": timeout}


# ============================================================
# 第 3 步：try / except / else / finally 全家桶
# ============================================================

def load_json_file(filepath: str) -> dict:
    """
    完整演示 try/except/else/finally 四种块的分工：
      try     : 可能出错的代码
      except  : 出错后处理（可以多个，从具体到宽泛）
      else    : 没出错才执行（和 try 区分开，意图更清晰）
      finally : 无论如何都执行（清理资源）
    """
    print(f"\n--- 加载文件: {filepath} ---")

    f = None
    try:
        # try: 可能抛出多种异常
        f = open(filepath, "r", encoding="utf-8")
        raw_text = f.read()
        data = json.loads(raw_text)   # 可能 JSONDecodeError

    except FileNotFoundError:
        # 精确捕获：文件不存在
        print("  [except] 文件不存在")
        return {}

    except json.JSONDecodeError as e:
        # 精确捕获：JSON 格式错误
        print(f"  [except] JSON 解析失败: {e}")
        return {}

    except Exception as e:
        # 宽泛兜底：其他未知错误
        print(f"  [except] 未知错误: {e}")
        return {}

    else:
        # else: try 块没抛任何异常才执行
        # 放在这里而不是 try 里，是为了不意外捕获 else 里抛的异常
        print(f"  [else]   文件加载成功，包含 {len(data)} 个顶层键")

    finally:
        # finally: 无论异常与否，一定执行
        # 资源清理的唯一正确位置
        if f is not None:
            f.close()
            print("  [finally] 文件已关闭")

    return data


# ============================================================
# 第 4 步：raise ... from —— 异常链，不丢失根因
# ============================================================

def parse_user_age(age_str: str) -> int:
    """
    raise ... from 保留原始异常链
    上层既能看到业务异常（InvalidTypeError），也能追溯到根因（ValueError）
    """
    try:
        age = int(age_str)
    except ValueError as e:
        # from e: 把原始 ValueError 链接到新异常上
        # 上层可以通过 __cause__ 追溯到根因
        raise InvalidTypeError("age", "int", type(age_str).__name__) from e

    if age < 0 or age > 150:
        raise OutOfRangeError("age", age, 0, 150)

    return age


# ============================================================
# 第 5 步：实战 —— 多级异常处理
# ============================================================

def demo():
    print("=" * 60)
    print("  EAFP + 异常处理 完整演示")
    print("=" * 60)

    # -------- 场景 1：EAFP vs LBYL 同输入对比 --------
    print("\n>> 场景 1：正常配置 —— 两种风格结果相同")
    valid_config = {"host": "127.0.0.1", "port": 8080, "timeout": 5}
    r1 = process_config_lbyl(valid_config)
    r2 = process_config_eafp(valid_config)
    print(f"  LBYL: {r1}")
    print(f"  EAFP: {r2}")

    # -------- 场景 2：EAFP 优雅处理缺 key --------
    print("\n>> 场景 2：缺 port —— EAFP 风格自动转换 KeyError -> MissingKeyError")
    bad_config = {"host": "localhost", "timeout": 5}
    try:
        process_config_eafp(bad_config)
    except ConfigError as e:
        print(f"  [ERR] {e}")

    # -------- 场景 3：try/except/else/finally --------
    print("\n>> 场景 3：加载不存在的文件 → FileNotFoundError")
    load_json_file("nonexistent.json")

    print("\n>> 场景 4：加载存在的文件 → else 执行")
    # 先创建一个临时 JSON 文件
    import os
    tmp_path = os.path.join(os.path.dirname(__file__) or ".", "_demo_config.json")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump({"host": "0.0.0.0", "port": 3000}, f)
    load_json_file(tmp_path)
    os.remove(tmp_path)

    # -------- 场景 4：raise ... from 异常链 --------
    print("\n>> 场景 5：raise ... from 保留异常链")
    try:
        parse_user_age("not_a_number")
    except InvalidTypeError as e:
        print(f"  [ERR] 业务异常: {e}")
        print(f"  [根因] __cause__: {e.__cause__}")

    # -------- 场景 5：统一捕获基类 --------
    print("\n>> 场景 6：except ConfigError 统一捕获所有子异常")
    test_inputs = [
        {"host": "x"},                              # MissingKeyError
        {"host": "x", "port": "abc"},              # InvalidTypeError
        {"host": "x", "port": 99999},              # OutOfRangeError
        {"host": "x", "port": 80},                 # OK
    ]
    for inp in test_inputs:
        try:
            result = process_config_eafp(inp)
            print(f"  [OK] {inp} -> {result}")
        except ConfigError as e:
            # 一个 except 接住所有 ConfigError 子类
            print(f"  [ERR] {type(e).__name__}: {e}")

    print("\n" + "=" * 60)
    print("  演示结束")
    print("=" * 60)


if __name__ == "__main__":
    demo()
