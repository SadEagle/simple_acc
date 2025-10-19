from decimal import Decimal

from datetime import date
from typing import Sequence

from pydantic import BaseModel, TypeAdapter

TupleAccums = TypeAdapter(Sequence["Accum"])
TupleDevices = TypeAdapter(Sequence["Device"])


class AccumCreate(BaseModel):
    name: str
    rated_voltage: Decimal
    residual_capacity: Decimal
    expiration_date: date
    device_id: int | None


class AccumUpdate(BaseModel):
    name: str | None = None
    rated_voltage: Decimal | None = None
    residual_capacity: Decimal | None = None
    expiration_date: date | None = None
    device_id: int | None = None


class Accum(AccumCreate):
    id: int


class DeviceCreate(BaseModel):
    name: str
    firmware_ver: str
    is_on: bool


class DeviceUpdate(BaseModel):
    name: str | None = None
    firmware_ver: str | None = None
    is_on: bool | None = None


class Device(DeviceCreate):
    id: int


class DeviceWithAccums(BaseModel):
    """Device with connected accums"""

    device: Device
    accums: tuple[Accum, ...]


class AccumWithDevice(BaseModel):
    """Accum with it's owner device"""

    device: Device
    accum: Accum | None


class Message(BaseModel):
    message: str


# NOTE: Need if TypeAdapter was defined before inner classes
# Ref https//docs.pydantic.dev/2.11/errors/usage_errors/#class-not-fully-defined
TupleAccums.rebuild()
TupleDevices.rebuild()
