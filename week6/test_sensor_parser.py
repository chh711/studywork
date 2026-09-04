"""sensor_parser 模块的 pytest 用例。"""

import pytest

from sensor_parser import (
    FrameFormatError,
    SensorParseError,
    SensorReading,
    ValueOutOfRangeError,
    parse_frame,
    safe_parse_frame,
)


def test_parse_single_field() -> None:
    """正常解析单字段帧。"""
    readings = parse_frame("TEMP:23.5")
    assert readings == [SensorReading(sensor_type="TEMP", value=23.5, unit="celsius")]


def test_parse_multiple_fields() -> None:
    """正常解析多字段帧，顺序和值都应正确。"""
    readings = parse_frame("TEMP:23.5;HUM:60.1;PRES:1013.25")
    assert [r.sensor_type for r in readings] == ["TEMP", "HUM", "PRES"]
    assert [r.unit for r in readings] == ["celsius", "percent", "hpa"]
    assert readings[2].value == pytest.approx(1013.25)


def test_invalid_frame_raises_frame_format_error() -> None:
    """非法输入（缺少分隔符 / 数值无法解析）应抛出 FrameFormatError。"""
    with pytest.raises(FrameFormatError):
        parse_frame("TEMP23.5")  # 缺少 ':'
    with pytest.raises(FrameFormatError, match="无法解析"):
        parse_frame("TEMP:abc")  # 数值非法


def test_out_of_range_raises_and_is_caught_by_base_exception() -> None:
    """超量程应抛 ValueOutOfRangeError，且能被基类 SensorParseError 捕获。"""
    with pytest.raises(ValueOutOfRangeError):
        parse_frame("TEMP:999")
    with pytest.raises(SensorParseError):  # 子类异常可被基类捕获
        parse_frame("HUM:-1")


def test_safe_parse_frame_swallows_errors() -> None:
    """safe_parse_frame 对非法输入返回空列表，不抛异常。"""
    assert safe_parse_frame("BADFRAME") == []
    assert safe_parse_frame("") == []
    assert len(safe_parse_frame("PRES:1013")) == 1  # 合法输入仍正常解析
