from enum import Enum
from typing import Self


class Gender(Enum):
    m = 0, "Nam"
    f = 1, "Nữ"

    def __new__(cls, value: int, display_name: str) -> Self:
        self = object.__new__(cls)
        self._value_ = value
        self._add_value_alias_(display_name)
        return self

    def __init__(self, _, display_name: str):
        self.display_name = display_name
