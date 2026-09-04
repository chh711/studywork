"""传感器数据解析模块

将原始字符串帧（如 "TEMP:23.5;HUM:60.1"）解析为结构化的 SensorReading。
包含类型标注、异常处理和自定义异常。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


class SensorParseError(Exception):
    """传感器数据解析失败的基类异常。"""


class FrameFormatError(SensorParseError):
    """帧格式不合法（缺少分隔符、字段残缺等）。"""


class ValueOutOfRangeError(SensorParseError):
    """解析出的数值超出传感器允许范围。"""


@dataclass(frozen=True)
class SensorReading:
    """一条传感器读数。"""

    sensor_type: str
    value: float
    unit: str


# 传感器类型 -> (单位, 最小值, 最大值)
_SENSOR_SPECS: Mapping[str, tuple[str, float, float]] = {
    "TEMP": ("celsius", -40.0, 125.0),
    "HUM": ("percent", 0.0, 100.0),
    "PRES": ("hpa", 300.0, 1100.0),
}


def parse_frame(frame: str) -> list[SensorReading]:
    """解析一帧传感器数据，如 "TEMP:23.5;HUM:60.1"。

    Args:
        frame: 原始帧字符串，字段用 ";" 分隔，每个字段形如 "TYPE:VALUE"。

    Returns:
        SensorReading 列表。

    Raises:
        TypeError: frame 不是字符串。
        FrameFormatError: 帧为空、字段缺少 ":" 或数值无法解析。
        ValueOutOfRangeError: 数值超出该传感器的量程。
    """
    if not isinstance(frame, str):
        raise TypeError(f"frame 必须是 str，而不是 {type(frame).__name__}")
    if not frame.strip():
        raise FrameFormatError("帧为空")

    readings: list[SensorReading] = []
    for field in frame.split(";"):
        field = field.strip()
        if ":" not in field:
            raise FrameFormatError(f"字段 {field!r} 缺少 ':' 分隔符")
        sensor_type, _, raw_value = field.partition(":")
        sensor_type = sensor_type.strip().upper()

        try:
            value = float(raw_value)
        except ValueError as exc:
            raise FrameFormatError(f"字段 {field!r} 的数值 {raw_value!r} 无法解析") from exc

        spec = _SENSOR_SPECS.get(sensor_type)
        if spec is None:
            raise FrameFormatError(f"未知传感器类型: {sensor_type!r}")
        unit, low, high = spec
        if not (low <= value <= high):
            raise ValueOutOfRangeError(
                f"{sensor_type} 数值 {value} 超出量程 [{low}, {high}]"
            )
        readings.append(SensorReading(sensor_type=sensor_type, value=value, unit=unit))
    return readings


def safe_parse_frame(frame: str) -> list[SensorReading]:
    """解析帧，失败时返回空列表而不是抛异常（异常处理示例）。"""
    try:
        return parse_frame(frame)
    except SensorParseError as exc:
        print(f"[警告] 解析失败，已丢弃该帧: {exc}")
        return []


if __name__ == "__main__":
    for reading in parse_frame("TEMP:23.5;HUM:60.1"):
        print(reading)
    safe_parse_frame("BADFRAME")
