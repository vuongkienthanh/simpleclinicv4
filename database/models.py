import datetime as dt
import enum
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, ClassVar, Self, final


class Gender(enum.Enum):
    m = 0, "Nam"
    f = 1, "Nữ"

    def __new__(cls, value: int, display_name: str) -> Self:
        self = object.__new__(cls)
        self._value_ = value
        self._add_value_alias_(display_name)  # pyright: ignore[reportAttributeAccessIssue] remove when typeshed include stubs
        return self

    def __init__(self, value: int, display_name: str):
        self.display_name = display_name


@dataclass(slots=True, frozen=True)
class BASEMODEL:
    """
    Base Class for derived sql table
    - `__table_name__`: name of table in sqlite database
    - `__fields__`: names of fields for sql query insert/update
    """

    __tablename__: ClassVar[str]
    __fields__: ClassVar[tuple[str, ...]]
    id: int

    @classmethod
    def parse(cls, row: Mapping[str, Any]) -> Self:
        return cls(**row)

    @classmethod
    def commna_joined_fields(cls) -> str:
        return ",".join(cls.__fields__)

    @classmethod
    def named_style_placeholders(cls) -> str:
        return ",".join([f":{f}" for f in cls.__fields__])


@final
@dataclass(slots=True, frozen=True)
class Patient(BASEMODEL):
    __tablename__ = "patients"
    __fields__ = (
        "name",
        "gender",
        "birthdate",
        "address",
        "phone",
        "past_history",
    )
    name: str
    gender: Gender
    birthdate: dt.date
    address: str | None = None
    phone: str | None = None
    past_history: str | None = None


@final
@dataclass(slots=True, frozen=True)
class Visit(BASEMODEL):
    __tablename__ = "visits"
    __fields__ = (
        "patient_id",
        "diagnosis",
        "weight",
        "days",
        "check_after_n_days",
        "price",
        "note",
        "follow_note",
        "misc_data",
    )
    patient_id: int
    exam_datetime: dt.datetime
    diagnosis: str
    weight: int
    days: int
    check_after_n_days: int
    price: int
    note: str | None = None
    follow_note: str | None = None
    misc_data: dict[str, Any] | None = None


@final
@dataclass(slots=True, frozen=True)
class Queue(BASEMODEL):
    __tablename__ = "queue"
    __fields__ = ("patient_id",)
    patient_id: int
    added_datetime: dt.datetime


@final
@dataclass(slots=True, frozen=True)
class Warehouse(BASEMODEL):
    __tablename__ = "warehouse"
    __fields__ = (
        "name",
        "element",
        "quantity",
        "usage",
        "usage_unit",
        "sale_unit",
        "purchase_price",
        "sale_price",
        "expire_date",
        "note",
    )
    name: str
    element: str
    quantity: int
    usage: str
    usage_unit: str
    purchase_price: int
    sale_price: int
    sale_unit: str | None = None
    expire_date: dt.date | None = None
    note: str | None = None


@final
@dataclass(slots=True, frozen=True)
class LineDrug(BASEMODEL):
    __tablename__ = "linedrugs"
    __fields__ = (
        "warehouse_id",
        "times",
        "dose",
        "quantity",
        "visit_id",
        "usage_note",
    )
    warehouse_id: int
    times: int
    dose: str
    quantity: int
    visit_id: int
    usage_note: str | None = None


@final
@dataclass(slots=True, frozen=True)
class Procedure(BASEMODEL):
    __tablename__ = "procedures"
    __fields__ = ("name", "price")
    name: str
    price: int


@final
@dataclass(slots=True, frozen=True)
class LineProcedure(BASEMODEL):
    __tablename__ = "lineprocedures"
    __fields__ = ("procedure_id", "visit_id")
    procedure_id: int
    visit_id: int
