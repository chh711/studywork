"""演示 SensorReading 解析 —— 正常与异常场景。"""

from sensor_reading import SensorReading, SensorParseException

SAMPLES = [
    "2024-08-07 14:30:00,DEV-001,23.56",        # ✓ 正常
    "2025-01-15 08:00:00,DEV-002,-5.0",          # ✓ 正常（负值）
    None,                                         # ✗ null
    "",                                           # ✗ 空白
    "bad-date,DEV-003,10.0",                      # ✗ 时间戳非法
    "2024-08-07 14:30:00,,10.0",                  # ✗ 设备号为空
    "2024-08-07 14:30:00,DEV-004,abc",            # ✗ 数值非法
    "only-two,fields",                            # ✗ 字段数不足
]

for line in SAMPLES:
    try:
        r = SensorReading.parse(line)
        print(f"[OK] 解析成功: {r}")
    except SensorParseException as e:
        print(f"[FAIL] {e}")