from dataclasses import dataclass
from datetime import datetime

# ---------------------------------------------------------------------------
# 自定义异常
# ---------------------------------------------------------------------------

class SensorParseException(Exception):
    """传感器记录解析异常，携带原始输入行以便定位问题。"""

    def __init__(self, message: str, raw_line: str | None = None) -> None:
        super().__init__(message)
        self.raw_line = raw_line

    def __str__(self) -> str:
        base = super().__str__()
        if self.raw_line is not None:
            return f"{base}  |  原始行: {self.raw_line!r}"
        return base


# ---------------------------------------------------------------------------
# SensorReading
# ---------------------------------------------------------------------------

# 约定时间戳格式
_TIMESTAMP_FMT = "%Y-%m-%d %H:%M:%S"


@dataclass(frozen=True)
class SensorReading:
    """传感器读数记录：时间戳、设备号、数值。

    原始记录格式（CSV 行，逗号分隔）::

        2024-08-07 14:30:00,DEV-001,23.56
    """

    timestamp: datetime
    device_id: str
    value: float

    # ---- 静态工厂方法 ----

    @staticmethod
    def parse(line: str) -> "SensorReading":
        """从一行传感器记录解析出 SensorReading 对象。

        Raises:
            SensorParseException: 格式非法或字段值无效时抛出。
        """
        if line is None or line.strip() == "":
            raise SensorParseException("输入行不能为 None 或空白", line)

        parts = line.split(",", maxsplit=-1)
        if len(parts) != 3:
            raise SensorParseException(
                f"期望 3 个字段（时间戳,设备号,数值），实际得到 {len(parts)} 个",
                line,
            )

        raw_ts, raw_dev, raw_val = (p.strip() for p in parts)

        # 1. 解析时间戳
        timestamp = _parse_timestamp(raw_ts, line)

        # 2. 校验设备号
        device_id = _validate_device_id(raw_dev, line)

        # 3. 解析数值
        value = _parse_value(raw_val, line)

        return SensorReading(timestamp, device_id, value)


# ---- 各字段解析与校验 ----

def _parse_timestamp(raw: str, line: str | None) -> datetime:
    try:
        return datetime.strptime(raw, _TIMESTAMP_FMT)
    except ValueError as exc:
        raise SensorParseException(
            f"时间戳格式非法，期望 {_TIMESTAMP_FMT!r}，实际: {raw!r}", line
        ) from exc


def _validate_device_id(raw: str, line: str | None) -> str:
    if not raw:
        raise SensorParseException("设备号不能为空", line)
    # 可扩展更多校验：长度、字符集等
    return raw


def _parse_value(raw: str, line: str | None) -> float:
    try:
        return float(raw)
    except ValueError as exc:
        raise SensorParseException(f"传感器数值无法解析为 float: {raw!r}", line) from exc