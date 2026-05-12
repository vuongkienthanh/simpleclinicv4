from lib.enums import Gender
import wx

from dataclasses import dataclass
from typing import ClassVar, final


@dataclass(slots=True, frozen=True)
class BASEMODEL:
    __tablename__: ClassVar[str]


@final
@dataclass(slots=True, frozen=True)
class Patient(BASEMODEL):
    __tablename__ = "patients"
    name: str
    gender: Gender
    birthdate: wx.DateTime
    past_history: str


@final
@dataclass(slots=True, frozen=True)
class Visit(BASEMODEL):
    __tablename__ = "visits"
    patient_id: int
    weight: int
    medical_history: str
    diagnosis: str
    days: int
    note: str
    price: int


@final
@dataclass(slots=True, frozen=True)
class SeenToday(BASEMODEL):
    __tablename__ = "seentoday"
    visit_id: int


@final
@dataclass(slots=True, frozen=True)
class MedicineStore(BASEMODEL):
    __tablename__ = "medicine_store"
    name: str
    element: str
    quantity: int
    route: str
    usage_unit: str
    selling_unit: str
    cost_price: int
    selling_price: int


@final
@dataclass(slots=True, frozen=True)
class Medicine(BASEMODEL):
    __tablename__ = "medicine"
    medicine_id: int
    visit_id: int
    times: int
    dose: str
    quantity: int
    usage_note: str


@final
@dataclass(slots=True, frozen=True)
class ServiceStore(BASEMODEL):
    __tablename__ = "service_store"
    name: str
    price: int


@final
@dataclass(slots=True, frozen=True)
class Service(BASEMODEL):
    __tablename__ = "services"
    service_id: int
    visit_id: int
    quantity: int
