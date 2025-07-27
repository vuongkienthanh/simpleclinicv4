from enum import Enum
from typing import Self


class Gender(Enum):
    m = 0, "Nam"
    f = 1, "Nữ"

    def __new__(cls, value: int, display_name: str) -> Self:
        self = object.__new__(cls)
        self._value_ = value
        self._add_value_alias_(display_name)  # pyright: ignore[reportAttributeAccessIssue] remove when typeshed include stubs
        return self

    def __init__(self, _, display_name: str):
        self.display_name = display_name


class VNWeekday(Enum):
    T2 = 0, "Thứ hai"
    T3 = 1, "Thứ ba"
    T4 = 2, "Thứ tư"
    T5 = 3, "Thứ năm"
    T6 = 4, "Thứ sáu"
    T7 = 5, "Thứ bảy"
    CN = 6, "Chủ nhật"

    def __new__(cls, value: int, _: str) -> Self:
        self = object.__new__(cls)
        self._value_ = value
        return self

    def __init__(self, _, display_name: str):
        self.display_name = display_name
