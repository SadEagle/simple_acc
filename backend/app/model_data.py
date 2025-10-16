from decimal import Decimal

from pydantic import BaseModel, TypeAdapter

TupleAccums = TypeAdapter(tuple["Accum", ...])
TupleDevices = TypeAdapter(tuple["Device", ...])


class AccumCreate(BaseModel):
    name: str
    rated_voltage: Decimal
    residual_capacity: Decimal
    device_id: int | None


class AccumUpdate(BaseModel):
    name: str | None
    rated_voltage: Decimal | None
    residual_capacity: Decimal | None
    device_id: int | None


class Accum(AccumCreate):
    id: int


class DeviceCreate(BaseModel):
    name: str
    firmware_ver: str
    is_on: bool


class DeviceUpdate(BaseModel):
    name: str | None
    firmware_ver: str | None
    is_on: bool | None


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
